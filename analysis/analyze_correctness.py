#!/usr/bin/env python3
"""Analyze correctness results produced by ``test_harness/harness.py``.

The primary score is pass@1 over judge-supported tasks.  A strict score over
all tasks is also reported so unsupported harness formats remain visible.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = PROJECT_ROOT / "analysis" / "outputs" / "correctness_results.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "analysis" / "outputs"

MODELS = (
    ("Qwen3-0.6B", "0.6B", 0.6),
    ("Qwen3-1.7B", "1.7B", 1.7),
    ("Qwen3-4B", "4B", 4.0),
    ("Qwen3-8B", "8B", 8.0),
)

CONFIGS = (
    ("no_thinking_sampled_4k", "No-think 4K", False, 4096),
    ("thinking_4k_presence_1_0", "Think 4K", True, 4096),
    ("thinking_8k_presence_1_0", "Think 8K", True, 8192),
    ("thinking_12k_presence_1_0", "Think 12K", True, 12000),
    ("thinking_24k_presence_1_0", "Think 24K", True, 24000),
)

MODEL_ORDER = [model for model, _, _ in MODELS]
MODEL_LABELS = {model: label for model, label, _ in MODELS}
MODEL_SIZES = {model: size for model, _, size in MODELS}
CONFIG_ORDER = [config for config, _, _, _ in CONFIGS]
CONFIG_LABELS = {config: label for config, label, _, _ in CONFIGS}
CONFIG_BUDGETS = {config: budget for config, _, _, budget in CONFIGS}
THINKING_CONFIGS = [config for config, _, thinking, _ in CONFIGS if thinking]

EXECUTED_STATUSES = {"accepted", "wrong_answer", "runtime_error", "timeout"}
STATUS_ORDER = (
    "accepted",
    "wrong_answer",
    "runtime_error",
    "timeout",
    "incomplete_thinking",
    "generation_error",
    "syntax_error",
    "empty_code",
    "unsupported_test_format",
    "worker_error",
)

REQUIRED_COLUMNS = {
    "task_id",
    "dataset",
    "model",
    "config",
    "status",
}


def percent(numerator: int | float, denominator: int | float) -> float:
    return 100.0 * numerator / denominator if denominator else math.nan


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return math.nan, math.nan
    proportion = successes / total
    denominator = 1.0 + z * z / total
    center = (proportion + z * z / (2.0 * total)) / denominator
    margin = (
        z
        * math.sqrt(
            proportion * (1.0 - proportion) / total
            + z * z / (4.0 * total * total)
        )
        / denominator
    )
    return 100.0 * (center - margin), 100.0 * (center + margin)


def pearson_r(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(xs) != len(ys):
        return math.nan
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    if np.allclose(x, x[0]) or np.allclose(y, y[0]):
        return math.nan
    return float(np.corrcoef(x, y)[0, 1])


def load_and_validate(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns in {path}: {sorted(missing)}")
    if frame.empty:
        raise ValueError(f"No correctness rows in {path}")
    if frame[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Required correctness fields contain missing values")

    unknown_models = sorted(set(frame["model"]) - set(MODEL_ORDER))
    unknown_configs = sorted(set(frame["config"]) - set(CONFIG_ORDER))
    unknown_datasets = sorted(set(frame["dataset"]) - {"apps", "lcb"})
    if unknown_models or unknown_configs or unknown_datasets:
        raise ValueError(
            "Unexpected result labels: "
            f"models={unknown_models}, configs={unknown_configs}, "
            f"datasets={unknown_datasets}"
        )

    key = ["task_id", "model", "config"]
    duplicates = frame.duplicated(key, keep=False)
    if duplicates.any():
        example = frame.loc[duplicates, key].iloc[0].to_dict()
        raise ValueError(f"Duplicate correctness result: {example}")

    expected_cells = len(MODELS) * len(CONFIGS)
    per_task = frame.groupby("task_id", sort=False).size()
    if not per_task.eq(expected_cells).all():
        bad_task = str(per_task[~per_task.eq(expected_cells)].index[0])
        raise ValueError(
            f"Task {bad_task!r} does not have exactly {expected_cells} results"
        )

    task_dataset_counts = frame.groupby("task_id")["dataset"].nunique()
    if not task_dataset_counts.eq(1).all():
        raise ValueError("At least one task_id appears in multiple datasets")

    frame = frame.copy()
    frame["accepted"] = frame["status"].eq("accepted")
    frame["supported"] = frame["status"].ne("unsupported_test_format")
    frame["executed"] = frame["status"].isin(EXECUTED_STATUSES)
    frame["model_label"] = frame["model"].map(MODEL_LABELS)
    frame["config_label"] = frame["config"].map(CONFIG_LABELS)
    return frame


def scope_frames(frame: pd.DataFrame):
    yield "combined", frame
    yield "apps", frame[frame["dataset"].eq("apps")]
    yield "lcb", frame[frame["dataset"].eq("lcb")]


def make_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for scope, scoped in scope_frames(frame):
        for model, model_label, model_size in MODELS:
            for config, config_label, thinking, budget in CONFIGS:
                cell = scoped[
                    scoped["model"].eq(model) & scoped["config"].eq(config)
                ]
                total = len(cell)
                supported = int(cell["supported"].sum())
                accepted = int(cell["accepted"].sum())
                executed = int(cell["executed"].sum())
                ci_low, ci_high = wilson_interval(accepted, supported)
                row: dict[str, object] = {
                    "scope": scope,
                    "model": model_label,
                    "model_directory": model,
                    "model_parameters_b": model_size,
                    "config": config_label,
                    "config_directory": config,
                    "thinking": thinking,
                    "max_tokens": budget,
                    "rows": total,
                    "supported_rows": supported,
                    "coverage_pct": percent(supported, total),
                    "accepted": accepted,
                    "strict_pass_rate_pct": percent(accepted, total),
                    "supported_pass_rate_pct": percent(accepted, supported),
                    "supported_pass_ci95_low_pct": ci_low,
                    "supported_pass_ci95_high_pct": ci_high,
                    "executed_rows": executed,
                    "execution_rate_pct": percent(executed, supported),
                    "executed_pass_rate_pct": percent(accepted, executed),
                }
                for status in STATUS_ORDER:
                    row[f"status_{status}"] = int(cell["status"].eq(status).sum())
                rows.append(row)
    return pd.DataFrame(rows)


def matrix_for(
    summary: pd.DataFrame,
    *,
    scope: str,
    metric: str,
) -> pd.DataFrame:
    subset = summary[summary["scope"].eq(scope)]
    matrix = subset.pivot(index="model", columns="config", values=metric)
    return matrix.reindex(
        index=[label for _, label, _ in MODELS],
        columns=[label for _, label, _, _ in CONFIGS],
    )


def make_status_counts(frame: pd.DataFrame) -> pd.DataFrame:
    counts = (
        frame.groupby(["dataset", "model_label", "config_label", "status"])
        .size()
        .rename("count")
        .reset_index()
    )
    totals = counts.groupby(
        ["dataset", "model_label", "config_label"]
    )["count"].transform("sum")
    counts["rate_pct"] = 100.0 * counts["count"] / totals
    return counts.sort_values(
        ["dataset", "model_label", "config_label", "status"]
    )


def make_paired_comparison(frame: pd.DataFrame) -> pd.DataFrame:
    no_think = CONFIGS[0][0]
    think_4k = CONFIGS[1][0]
    rows: list[dict[str, object]] = []

    for scope, scoped in scope_frames(frame):
        for model, model_label, _ in MODELS:
            pairs = scoped[
                scoped["model"].eq(model)
                & scoped["config"].isin([no_think, think_4k])
            ].pivot(index="task_id", columns="config", values="status")
            pairs = pairs[
                pairs[no_think].ne("unsupported_test_format")
                & pairs[think_4k].ne("unsupported_test_format")
            ]
            no_pass = pairs[no_think].eq("accepted")
            think_pass = pairs[think_4k].eq("accepted")
            rows.append(
                {
                    "scope": scope,
                    "model": model_label,
                    "paired_tasks": len(pairs),
                    "both_pass": int((no_pass & think_pass).sum()),
                    "no_think_only_pass": int((no_pass & ~think_pass).sum()),
                    "think_4k_only_pass": int((~no_pass & think_pass).sum()),
                    "neither_pass": int((~no_pass & ~think_pass).sum()),
                    "no_think_pass_rate_pct": 100.0 * float(no_pass.mean()),
                    "think_4k_pass_rate_pct": 100.0 * float(think_pass.mean()),
                    "think_4k_delta_pct_points": 100.0
                    * float(think_pass.mean() - no_pass.mean()),
                }
            )
    return pd.DataFrame(rows)


def make_budget_trends(summary: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    log_budgets = [math.log2(CONFIG_BUDGETS[config]) for config in THINKING_CONFIGS]
    for scope in ("combined", "apps", "lcb"):
        for model, model_label, _ in MODELS:
            cell_rows = summary[
                summary["scope"].eq(scope)
                & summary["model_directory"].eq(model)
                & summary["config_directory"].isin(THINKING_CONFIGS)
            ].set_index("config_directory")
            rates = [
                float(cell_rows.loc[config, "supported_pass_rate_pct"])
                for config in THINKING_CONFIGS
            ]
            best_index = int(np.argmax(rates))
            rows.append(
                {
                    "scope": scope,
                    "model": model_label,
                    "think_4k_pass_rate_pct": rates[0],
                    "think_8k_pass_rate_pct": rates[1],
                    "think_12k_pass_rate_pct": rates[2],
                    "think_24k_pass_rate_pct": rates[3],
                    "pearson_r_log2_budget": pearson_r(log_budgets, rates),
                    "monotonic_nondecreasing": all(
                        left <= right for left, right in zip(rates, rates[1:])
                    ),
                    "best_thinking_budget": CONFIG_LABELS[
                        THINKING_CONFIGS[best_index]
                    ],
                    "best_thinking_pass_rate_pct": rates[best_index],
                }
            )
    return pd.DataFrame(rows)


def make_model_size_trends(summary: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    log_sizes = [math.log2(size) for _, _, size in MODELS]
    for scope in ("combined", "apps", "lcb"):
        for config, config_label, _, _ in CONFIGS:
            cell_rows = summary[
                summary["scope"].eq(scope)
                & summary["config_directory"].eq(config)
            ].set_index("model_directory")
            rates = [
                float(cell_rows.loc[model, "supported_pass_rate_pct"])
                for model in MODEL_ORDER
            ]
            best_index = int(np.argmax(rates))
            rows.append(
                {
                    "scope": scope,
                    "config": config_label,
                    "pass_0_6b_pct": rates[0],
                    "pass_1_7b_pct": rates[1],
                    "pass_4b_pct": rates[2],
                    "pass_8b_pct": rates[3],
                    "pearson_r_log2_model_size": pearson_r(log_sizes, rates),
                    "monotonic_nondecreasing": all(
                        left <= right for left, right in zip(rates, rates[1:])
                    ),
                    "best_model": MODELS[best_index][1],
                    "best_pass_rate_pct": rates[best_index],
                }
            )
    return pd.DataFrame(rows)


def annotate_heatmap(axis, matrix: pd.DataFrame) -> None:
    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            value = float(matrix.iloc[row_index, column_index])
            color = "white" if value >= 35.0 else "black"
            axis.text(
                column_index,
                row_index,
                f"{value:.1f}",
                ha="center",
                va="center",
                color=color,
                fontsize=9,
            )


def plot_heatmaps(summary: pd.DataFrame, output_path: Path) -> None:
    figure, axes = plt.subplots(1, 3, figsize=(18, 4.8), constrained_layout=True)
    image = None
    for axis, scope, title in zip(
        axes,
        ("combined", "apps", "lcb"),
        ("Combined", "APPS", "LCB"),
    ):
        matrix = matrix_for(
            summary,
            scope=scope,
            metric="supported_pass_rate_pct",
        )
        image = axis.imshow(matrix.to_numpy(), cmap="viridis", vmin=0, vmax=60)
        annotate_heatmap(axis, matrix)
        axis.set_title(title)
        axis.set_xticks(range(len(matrix.columns)), matrix.columns, rotation=35, ha="right")
        axis.set_yticks(range(len(matrix.index)), matrix.index)
        axis.set_xlabel("Inference configuration")
        axis.set_ylabel("Model")

    assert image is not None
    colorbar = figure.colorbar(image, ax=axes, shrink=0.88)
    colorbar.set_label("Pass@1 on judge-supported tasks (%)")
    figure.suptitle("Qwen3 code correctness by model size and thinking budget")
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def plot_status_breakdown(frame: pd.DataFrame, output_path: Path) -> None:
    display_statuses = [status for status in STATUS_ORDER if status != "worker_error"]
    colors = {
        "accepted": "#2ca02c",
        "wrong_answer": "#d62728",
        "runtime_error": "#ff7f0e",
        "timeout": "#9467bd",
        "incomplete_thinking": "#7f7f7f",
        "generation_error": "#8c564b",
        "syntax_error": "#e377c2",
        "empty_code": "#bcbd22",
        "unsupported_test_format": "#17becf",
    }
    figure, axes = plt.subplots(2, 2, figsize=(14, 10), sharey=True, constrained_layout=True)
    for axis, (model, model_label, _) in zip(axes.flat, MODELS):
        subset = frame[frame["model"].eq(model)]
        table = pd.crosstab(subset["config_label"], subset["status"])
        table = table.reindex(
            index=[label for _, label, _, _ in CONFIGS],
            columns=display_statuses,
            fill_value=0,
        )
        percentages = 100.0 * table.div(table.sum(axis=1), axis=0)
        bottom = np.zeros(len(percentages))
        x_values = np.arange(len(percentages))
        for status in display_statuses:
            values = percentages[status].to_numpy()
            axis.bar(
                x_values,
                values,
                bottom=bottom,
                label=status,
                color=colors[status],
            )
            bottom += values
        axis.set_title(model_label)
        axis.set_xticks(x_values, percentages.index, rotation=30, ha="right")
        axis.set_ylim(0, 100)
        axis.set_ylabel("Share of all tasks (%)")

    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="outside lower center", ncol=5)
    figure.suptitle("Correctness and failure-mode composition")
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def plot_scaling(summary: pd.DataFrame, output_path: Path) -> None:
    combined = summary[summary["scope"].eq("combined")]
    figure, axes = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)

    model_sizes = [size for _, _, size in MODELS]
    for config, config_label, _, _ in CONFIGS:
        cells = combined[combined["config_directory"].eq(config)].set_index(
            "model_directory"
        )
        rates = [
            float(cells.loc[model, "supported_pass_rate_pct"])
            for model in MODEL_ORDER
        ]
        axes[0].plot(model_sizes, rates, marker="o", label=config_label)
    axes[0].set_xscale("log", base=2)
    axes[0].set_xticks(model_sizes, [label for _, label, _ in MODELS])
    axes[0].set_xlabel("Model size")
    axes[0].set_ylabel("Pass@1 on supported tasks (%)")
    axes[0].set_title("Scaling with model size")
    axes[0].grid(alpha=0.25)
    axes[0].legend(fontsize=8)

    thinking_budgets = [CONFIG_BUDGETS[config] for config in THINKING_CONFIGS]
    for model, model_label, _ in MODELS:
        cells = combined[combined["model_directory"].eq(model)].set_index(
            "config_directory"
        )
        rates = [
            float(cells.loc[config, "supported_pass_rate_pct"])
            for config in THINKING_CONFIGS
        ]
        axes[1].plot(thinking_budgets, rates, marker="o", label=model_label)
    axes[1].set_xscale("log", base=2)
    axes[1].set_xticks(thinking_budgets, ["4K", "8K", "12K", "24K"])
    axes[1].set_xlabel("Maximum thinking tokens")
    axes[1].set_ylabel("Pass@1 on supported tasks (%)")
    axes[1].set_title("Scaling with thinking budget")
    axes[1].grid(alpha=0.25)
    axes[1].legend()

    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def markdown_matrix(matrix: pd.DataFrame) -> list[str]:
    lines = [
        "| Model | " + " | ".join(matrix.columns) + " |",
        "|---|" + "---:|" * len(matrix.columns),
    ]
    for model, row in matrix.iterrows():
        values = " | ".join(f"{float(value):.2f}%" for value in row)
        lines.append(f"| {model} | {values} |")
    return lines


def make_report(
    frame: pd.DataFrame,
    summary: pd.DataFrame,
    paired: pd.DataFrame,
    budgets: pd.DataFrame,
    model_trends: pd.DataFrame,
) -> str:
    total_rows = len(frame)
    tasks = frame["task_id"].nunique()
    accepted = int(frame["accepted"].sum())
    supported = int(frame["supported"].sum())
    executed = int(frame["executed"].sum())
    unsupported_tasks = frame.loc[
        ~frame["supported"], "task_id"
    ].nunique()
    status_counts = frame["status"].value_counts()

    combined_summary = summary[summary["scope"].eq("combined")]
    best = combined_summary.loc[
        combined_summary["supported_pass_rate_pct"].idxmax()
    ]
    matrix = matrix_for(
        summary,
        scope="combined",
        metric="supported_pass_rate_pct",
    )
    apps_matrix = matrix_for(
        summary,
        scope="apps",
        metric="supported_pass_rate_pct",
    )
    lcb_matrix = matrix_for(
        summary,
        scope="lcb",
        metric="supported_pass_rate_pct",
    )

    lines = [
        "# Qwen3 correctness analysis",
        "",
        "## Executive summary",
        "",
        f"The harness evaluated {total_rows:,} generations from {tasks:,} tasks across 20 model/configuration cells. "
        f"It accepted {accepted:,} generations: a strict all-task pass rate of {percent(accepted, total_rows):.2f}% and a judge-supported pass rate of {percent(accepted, supported):.2f}%.",
        "",
        f"The best cell is **{best['model']} / {best['config']}** at **{float(best['supported_pass_rate_pct']):.2f}%** ({int(best['accepted']):,}/{int(best['supported_rows']):,} supported tasks).",
        "",
        "The central pattern is not a simple `larger model = better` law. More thinking budget strongly helps through 4B, but 8B stops improving after 12K and falls behind 4B at 12K and 24K because high-budget generation failures offset its stronger conditional solutions.",
        "",
        "## Coverage and denominators",
        "",
        f"- Strict denominator: all {total_rows:,} rows.",
        f"- Judge-supported denominator: {supported:,} rows ({percent(supported, total_rows):.2f}% coverage).",
        f"- Unsupported coverage: {unsupported_tasks} APPS tasks use non-string/function-call-style cases; this creates {total_rows - supported:,} unsupported rows, exactly the same tasks in every cell.",
        f"- Executed denominator: {executed:,} rows reached a test subprocess. Conditional pass rate among those rows is {percent(accepted, executed):.2f}%, but this is selection-biased and is not the primary score.",
        "",
        "Because unsupported tasks are identical across all cells, excluding them preserves matched comparisons. The primary tables below therefore use judge-supported pass@1.",
        "",
        "## Combined pass@1 matrix",
        "",
        *markdown_matrix(matrix),
        "",
        "![Combined, APPS, and LCB correctness heatmaps](correctness_heatmaps.png)",
        "",
        "## Dataset-specific matrices",
        "",
        "### APPS",
        "",
        *markdown_matrix(apps_matrix),
        "",
        "### LCB",
        "",
        *markdown_matrix(lcb_matrix),
        "",
        "## Thinking versus no-thinking at the same 4K cap",
        "",
        "This is a paired comparison on the same supported tasks. `Only pass` counts tasks solved by one configuration but not the other.",
        "",
        "| Model | No-think pass | Think 4K pass | Delta | No-think only | Think only | Both pass |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    paired_combined = paired[paired["scope"].eq("combined")]
    for _, row in paired_combined.iterrows():
        lines.append(
            f"| {row['model']} | {float(row['no_think_pass_rate_pct']):.2f}% | "
            f"{float(row['think_4k_pass_rate_pct']):.2f}% | "
            f"{float(row['think_4k_delta_pct_points']):+.2f} pp | "
            f"{int(row['no_think_only_pass']):,} | "
            f"{int(row['think_4k_only_pass']):,} | "
            f"{int(row['both_pass']):,} |"
        )

    lines.extend(
        [
            "",
            "Think 4K helps the 0.6B and 1.7B models, but hurts the 4B and 8B models. The 4K thinking cap frequently ends before `</think>`, so extra reasoning is useful only when enough of it reaches executable code.",
            "",
            "## Failure composition",
            "",
            "| Status | Rows | Share of all rows |",
            "|---|---:|---:|",
        ]
    )
    for status in STATUS_ORDER:
        count = int(status_counts.get(status, 0))
        if count:
            lines.append(f"| `{status}` | {count:,} | {percent(count, total_rows):.2f}% |")

    lines.extend(
        [
            "",
            "![Correctness and failure-mode composition](correctness_status_breakdown.png)",
            "",
            "`incomplete_thinking`, `generation_error`, `syntax_error`, and `empty_code` fail before tests can establish semantic correctness. This is why end-to-end pass@1 is lower than correctness conditional on executable outputs.",
            "",
            "## Scaling relationships",
            "",
            "![Correctness scaling relationships](correctness_scaling.png)",
            "",
            "### Thinking-budget trends",
            "",
            "| Model | 4K | 8K | 12K | 24K | r vs log2 budget | Monotonic | Best |",
            "|---|---:|---:|---:|---:|---:|:---:|---:|",
        ]
    )
    combined_budgets = budgets[budgets["scope"].eq("combined")]
    for _, row in combined_budgets.iterrows():
        lines.append(
            f"| {row['model']} | {float(row['think_4k_pass_rate_pct']):.2f}% | "
            f"{float(row['think_8k_pass_rate_pct']):.2f}% | "
            f"{float(row['think_12k_pass_rate_pct']):.2f}% | "
            f"{float(row['think_24k_pass_rate_pct']):.2f}% | "
            f"{float(row['pearson_r_log2_budget']):.3f} | "
            f"{'yes' if bool(row['monotonic_nondecreasing']) else 'no'} | "
            f"{row['best_thinking_budget']} |"
        )

    lines.extend(
        [
            "",
            "### Model-size trends",
            "",
            "| Configuration | 0.6B | 1.7B | 4B | 8B | r vs log2 size | Monotonic | Best model |",
            "|---|---:|---:|---:|---:|---:|:---:|---:|",
        ]
    )
    combined_models = model_trends[model_trends["scope"].eq("combined")]
    for _, row in combined_models.iterrows():
        lines.append(
            f"| {row['config']} | {float(row['pass_0_6b_pct']):.2f}% | "
            f"{float(row['pass_1_7b_pct']):.2f}% | "
            f"{float(row['pass_4b_pct']):.2f}% | "
            f"{float(row['pass_8b_pct']):.2f}% | "
            f"{float(row['pearson_r_log2_model_size']):.3f} | "
            f"{'yes' if bool(row['monotonic_nondecreasing']) else 'no'} | "
            f"{row['best_model']} |"
        )

    lines.extend(
        [
            "",
            "These correlations contain only four aggregate points each. They describe the observed matrix; they are not evidence of a universal scaling law.",
            "",
            "## Interpretation limits",
            "",
            "- This is one generated answer per task/configuration, so the score is pass@1 rather than pass@k.",
            "- Output comparison is exact after trimming leading/trailing whitespace. It does not implement token-wise whitespace equivalence, special judges, or floating-point tolerance, so these are harness-defined correctness rates rather than official APPS/LCB leaderboard scores.",
            "- Each testcase has a two-second subprocess timeout. Programs exceeding it are counted as incorrect.",
            "- The 98 unsupported APPS tasks need a separate function-call evaluator before strict full-dataset accuracy can be claimed.",
            "- Conditional accuracy among executed programs excludes generation and normalization failures and should not replace end-to-end pass@1.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = load_and_validate(args.results)
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = make_summary(frame)
    status_counts = make_status_counts(frame)
    paired = make_paired_comparison(frame)
    budgets = make_budget_trends(summary)
    model_trends = make_model_size_trends(summary)

    summary.to_csv(output_dir / "correctness_summary.csv", index=False)
    status_counts.to_csv(output_dir / "correctness_status_counts.csv", index=False)
    paired.to_csv(
        output_dir / "correctness_paired_no_think_vs_think4k.csv",
        index=False,
    )
    budgets.to_csv(output_dir / "correctness_budget_correlations.csv", index=False)
    model_trends.to_csv(
        output_dir / "correctness_model_size_correlations.csv",
        index=False,
    )

    for scope in ("combined", "apps", "lcb"):
        suffix = "" if scope == "combined" else f"_{scope}"
        matrix_for(
            summary,
            scope=scope,
            metric="supported_pass_rate_pct",
        ).to_csv(
            output_dir / f"correctness_pass_rate_pct_matrix{suffix}.csv",
            index_label="Model",
        )
    matrix_for(
        summary,
        scope="combined",
        metric="strict_pass_rate_pct",
    ).to_csv(
        output_dir / "correctness_strict_pass_rate_pct_matrix.csv",
        index_label="Model",
    )

    plot_heatmaps(summary, output_dir / "correctness_heatmaps.png")
    plot_status_breakdown(frame, output_dir / "correctness_status_breakdown.png")
    plot_scaling(summary, output_dir / "correctness_scaling.png")
    report = make_report(frame, summary, paired, budgets, model_trends)
    (output_dir / "correctness_report.md").write_text(report, encoding="utf-8")

    print(f"Analyzed {len(frame):,} rows from {frame['task_id'].nunique():,} tasks")
    print(f"Wrote correctness analysis to {output_dir}")


if __name__ == "__main__":
    main()
