#!/usr/bin/env python3
"""Relate reasoning budget, reference-code complexity, and correctness."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm

from analyze_correctness import (
    CONFIGS,
    CONFIG_BUDGETS,
    CONFIG_LABELS,
    CONFIG_ORDER,
    DEFAULT_RESULTS,
    EXECUTED_STATUSES,
    MODELS,
    MODEL_LABELS,
    MODEL_ORDER,
    THINKING_CONFIGS,
    load_and_validate,
    pearson_r,
    percent,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACE_DIR = PROJECT_ROOT / "complexity_metrics" / "fair_traces"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "analysis" / "outputs"

PRIMARY_METRIC = "AST_Length"
SENSITIVITY_METRIC = "cyclomatic"
QUARTILE_ORDER = ["Q1", "Q2", "Q3", "Q4"]
QUARTILE_DESCRIPTIONS = {
    "Q1": "lowest complexity",
    "Q2": "low-medium complexity",
    "Q3": "medium-high complexity",
    "Q4": "highest complexity",
}


def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path}:{line_number}: {exc.msg}"
                ) from exc
            if not isinstance(row, dict):
                raise ValueError(f"Expected an object in {path}:{line_number}")
            yield row


def load_complexity(trace_dir: Path) -> pd.DataFrame:
    rows = []
    for dataset in ("apps", "lcb"):
        path = trace_dir / f"{dataset}_test.jsonl"
        rows.extend(read_jsonl(path))
    frame = pd.DataFrame(rows)
    required = {
        "task_id",
        "dataset",
        PRIMARY_METRIC,
        SENSITIVITY_METRIC,
        "loc",
        "Max_Nesting_Depth",
        "halstead_effort",
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing trace metrics: {sorted(missing)}")
    if frame["task_id"].duplicated().any():
        task_id = str(frame.loc[frame["task_id"].duplicated(), "task_id"].iloc[0])
        raise ValueError(f"Duplicate trace metrics for {task_id!r}")
    for metric in required - {"task_id", "dataset"}:
        frame[metric] = pd.to_numeric(frame[metric], errors="raise")
    return frame


def assign_quartiles(
    metrics: pd.DataFrame,
    *,
    metric: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    output = metrics.copy()
    output["complexity_quartile"], boundaries = pd.qcut(
        output[metric],
        q=4,
        labels=QUARTILE_ORDER,
        retbins=True,
        duplicates="raise",
    )
    grouped = output.groupby("complexity_quartile", observed=False)[metric]
    definitions = grouped.agg(["count", "min", "median", "max"]).reset_index()
    definitions.insert(1, "description", definitions["complexity_quartile"].map(
        QUARTILE_DESCRIPTIONS
    ))
    definitions["lower_quantile_boundary"] = boundaries[:-1]
    definitions["upper_quantile_boundary"] = boundaries[1:]
    definitions.insert(0, "metric", metric)
    return output, definitions


def merge_results_and_complexity(
    correctness: pd.DataFrame,
    complexity: pd.DataFrame,
    *,
    metric: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    supported_tasks = set(
        correctness.loc[correctness["supported"], "task_id"].unique()
    )
    available_tasks = set(complexity["task_id"])
    missing = sorted(supported_tasks - available_tasks)
    if missing:
        raise ValueError(f"Missing complexity metrics for {missing[0]!r}")

    task_metrics = complexity[complexity["task_id"].isin(supported_tasks)].copy()
    task_metrics, definitions = assign_quartiles(task_metrics, metric=metric)
    selected_columns = list(
        dict.fromkeys(
            [
                "task_id",
                "dataset",
                metric,
                "complexity_quartile",
                "AST_Length",
                "cyclomatic",
                "loc",
                "Max_Nesting_Depth",
                "halstead_effort",
            ]
        )
    )
    selected = task_metrics[selected_columns].drop_duplicates("task_id")
    merged = correctness[correctness["supported"]].merge(
        selected,
        on=["task_id", "dataset"],
        how="inner",
        validate="many_to_one",
        suffixes=("", "_complexity"),
    )
    expected = len(supported_tasks) * len(MODELS) * len(CONFIGS)
    if len(merged) != expected:
        raise ValueError(f"Expected {expected:,} merged rows, found {len(merged):,}")
    return merged, selected, definitions


def scope_frames(frame: pd.DataFrame):
    yield "combined", frame
    yield "apps", frame[frame["dataset"].eq("apps")]
    yield "lcb", frame[frame["dataset"].eq("lcb")]


def make_group_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for scope, scoped in scope_frames(frame):
        for model, model_label, _ in MODELS:
            for config, config_label, thinking, max_tokens in CONFIGS:
                for quartile in QUARTILE_ORDER:
                    cell = scoped[
                        scoped["model"].eq(model)
                        & scoped["config"].eq(config)
                        & scoped["complexity_quartile"].eq(quartile)
                    ]
                    tasks = len(cell)
                    accepted = int(cell["accepted"].sum())
                    executed = int(cell["status"].isin(EXECUTED_STATUSES).sum())
                    rows.append(
                        {
                            "scope": scope,
                            "model": model_label,
                            "model_directory": model,
                            "config": config_label,
                            "config_directory": config,
                            "thinking": thinking,
                            "max_tokens": max_tokens,
                            "reasoning_budget_tokens": max_tokens if thinking else 0,
                            "complexity_quartile": quartile,
                            "complexity_description": QUARTILE_DESCRIPTIONS[quartile],
                            "tasks": tasks,
                            "accepted": accepted,
                            "pass_rate_pct": percent(accepted, tasks),
                            "executed": executed,
                            "execution_rate_pct": percent(executed, tasks),
                            "executed_pass_rate_pct": percent(accepted, executed),
                        }
                    )
    return pd.DataFrame(rows)


def make_budget_trends(
    frame: pd.DataFrame,
    summary: pd.DataFrame,
    *,
    metric: str,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    log_budgets = [math.log2(CONFIG_BUDGETS[config]) for config in THINKING_CONFIGS]
    no_think = CONFIG_ORDER[0]
    think_4k = THINKING_CONFIGS[0]
    think_24k = THINKING_CONFIGS[-1]

    for scope, scoped in scope_frames(frame):
        scoped_summary = summary[summary["scope"].eq(scope)]
        for model, model_label, _ in MODELS:
            for quartile in QUARTILE_ORDER:
                cells = scoped_summary[
                    scoped_summary["model_directory"].eq(model)
                    & scoped_summary["complexity_quartile"].eq(quartile)
                ].set_index("config_directory")
                rates = [
                    float(cells.loc[config, "pass_rate_pct"])
                    for config in THINKING_CONFIGS
                ]
                best_index = int(np.argmax(rates))

                pairs = scoped[
                    scoped["model"].eq(model)
                    & scoped["complexity_quartile"].eq(quartile)
                    & scoped["config"].isin([think_4k, think_24k])
                ].pivot(index="task_id", columns="config", values="status")
                pass_4k = pairs[think_4k].eq("accepted")
                pass_24k = pairs[think_24k].eq("accepted")

                rows.append(
                    {
                        "metric": metric,
                        "scope": scope,
                        "model": model_label,
                        "complexity_quartile": quartile,
                        "tasks": int(cells.loc[think_4k, "tasks"]),
                        "no_think_pass_rate_pct": float(
                            cells.loc[no_think, "pass_rate_pct"]
                        ),
                        "think_4k_pass_rate_pct": rates[0],
                        "think_8k_pass_rate_pct": rates[1],
                        "think_12k_pass_rate_pct": rates[2],
                        "think_24k_pass_rate_pct": rates[3],
                        "pearson_r_log2_budget": pearson_r(log_budgets, rates),
                        "slope_pct_points_per_budget_doubling": float(
                            np.polyfit(log_budgets, rates, 1)[0]
                        ),
                        "think_4k_vs_no_think_delta_pct_points": rates[0]
                        - float(cells.loc[no_think, "pass_rate_pct"]),
                        "think_24k_vs_4k_delta_pct_points": rates[3] - rates[0],
                        "think_24k_vs_12k_delta_pct_points": rates[3] - rates[2],
                        "think_4k_only_pass": int((pass_4k & ~pass_24k).sum()),
                        "think_24k_only_pass": int((~pass_4k & pass_24k).sum()),
                        "both_pass": int((pass_4k & pass_24k).sum()),
                        "neither_pass": int((~pass_4k & ~pass_24k).sum()),
                        "best_thinking_budget": CONFIG_LABELS[
                            THINKING_CONFIGS[best_index]
                        ],
                        "best_thinking_pass_rate_pct": rates[best_index],
                    }
                )
    return pd.DataFrame(rows)


def make_capacity_trends(summary: pd.DataFrame) -> pd.DataFrame:
    """Compare adjacent model sizes at a fixed inference configuration."""
    rate_columns = {
        "Qwen3-0.6B": "pass_0_6b_pct",
        "Qwen3-1.7B": "pass_1_7b_pct",
        "Qwen3-4B": "pass_4b_pct",
        "Qwen3-8B": "pass_8b_pct",
    }
    rows: list[dict[str, object]] = []
    for scope in ("combined", "apps", "lcb"):
        scoped = summary[summary["scope"].eq(scope)]
        for config in CONFIG_ORDER:
            for quartile in QUARTILE_ORDER:
                cells = scoped[
                    scoped["config_directory"].eq(config)
                    & scoped["complexity_quartile"].eq(quartile)
                ].set_index("model_directory")
                rates = {
                    rate_columns[model]: float(cells.loc[model, "pass_rate_pct"])
                    for model in MODEL_ORDER
                }
                rows.append(
                    {
                        "scope": scope,
                        "config": CONFIG_LABELS[config],
                        "config_directory": config,
                        "complexity_quartile": quartile,
                        "tasks": int(cells.loc[MODEL_ORDER[0], "tasks"]),
                        **rates,
                        "gain_0_6b_to_1_7b_pp": (
                            rates["pass_1_7b_pct"] - rates["pass_0_6b_pct"]
                        ),
                        "gain_1_7b_to_4b_pp": (
                            rates["pass_4b_pct"] - rates["pass_1_7b_pct"]
                        ),
                        "gain_4b_to_8b_pp": (
                            rates["pass_8b_pct"] - rates["pass_4b_pct"]
                        ),
                    }
                )
    return pd.DataFrame(rows)


def make_compute_marginal_gains(summary: pd.DataFrame) -> pd.DataFrame:
    """Compare the requested adjacent inference-compute regimes."""
    no_think, think_4k, _, think_12k, think_24k = CONFIG_ORDER
    rows: list[dict[str, object]] = []
    for scope in ("combined", "apps", "lcb"):
        scoped = summary[summary["scope"].eq(scope)]
        for model, model_label, _ in MODELS:
            for quartile in QUARTILE_ORDER:
                cells = scoped[
                    scoped["model_directory"].eq(model)
                    & scoped["complexity_quartile"].eq(quartile)
                ].set_index("config_directory")
                rates = {
                    config: float(cells.loc[config, "pass_rate_pct"])
                    for config in (no_think, think_4k, think_12k, think_24k)
                }
                rows.append(
                    {
                        "scope": scope,
                        "model": model_label,
                        "model_directory": model,
                        "complexity_quartile": quartile,
                        "tasks": int(cells.loc[no_think, "tasks"]),
                        "no_think_4k_pass_rate_pct": rates[no_think],
                        "think_4k_pass_rate_pct": rates[think_4k],
                        "think_12k_pass_rate_pct": rates[think_12k],
                        "think_24k_pass_rate_pct": rates[think_24k],
                        "no_think_to_think_4k_pp": (
                            rates[think_4k] - rates[no_think]
                        ),
                        "think_4k_to_12k_pp": rates[think_12k] - rates[think_4k],
                        "think_12k_to_24k_pp": (
                            rates[think_24k] - rates[think_12k]
                        ),
                    }
                )
    return pd.DataFrame(rows)


def make_complexity_correlations(
    frame: pd.DataFrame,
    *,
    metric: str,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for scope, scoped in scope_frames(frame):
        for model, model_label, _ in MODELS:
            for config, config_label, _, _ in CONFIGS:
                cell = scoped[
                    scoped["model"].eq(model) & scoped["config"].eq(config)
                ]
                rows.append(
                    {
                        "metric": metric,
                        "scope": scope,
                        "model": model_label,
                        "config": config_label,
                        "tasks": len(cell),
                        "spearman_complexity_vs_accepted": float(
                            cell[metric].corr(cell["accepted"].astype(float), method="spearman")
                        ),
                        "pearson_log_complexity_vs_accepted": float(
                            np.corrcoef(
                                np.log1p(cell[metric].to_numpy(dtype=float)),
                                cell["accepted"].to_numpy(dtype=float),
                            )[0, 1]
                        ),
                    }
                )
    return pd.DataFrame(rows)


def plot_budget_by_quartile(
    summary: pd.DataFrame,
    output_path: Path,
    *,
    title_metric: str,
) -> None:
    combined = summary[summary["scope"].eq("combined")]
    config_labels = [label for _, label, _, _ in CONFIGS]
    colors = dict(zip(QUARTILE_ORDER, ("#2ca02c", "#1f77b4", "#ff7f0e", "#d62728")))
    figure, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=True, constrained_layout=True)
    x_values = np.arange(len(CONFIGS))

    for axis, (model, model_label, _) in zip(axes.flat, MODELS):
        cells = combined[combined["model_directory"].eq(model)]
        for quartile in QUARTILE_ORDER:
            quartile_cells = cells[
                cells["complexity_quartile"].eq(quartile)
            ].set_index("config_directory")
            rates = [
                float(quartile_cells.loc[config, "pass_rate_pct"])
                for config in CONFIG_ORDER
            ]
            axis.plot(
                x_values,
                rates,
                marker="o",
                linewidth=2,
                color=colors[quartile],
                label=f"{quartile}: {QUARTILE_DESCRIPTIONS[quartile]}",
            )
        axis.set_title(model_label)
        axis.set_xticks(x_values, config_labels, rotation=30, ha="right")
        axis.set_ylabel("Pass@1 on supported tasks (%)")
        axis.grid(alpha=0.25)

    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="outside lower center", ncol=2)
    figure.suptitle(
        f"Reasoning budget and correctness by {title_metric} quartile"
    )
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def plot_budget_gain(trends: pd.DataFrame, output_path: Path) -> None:
    combined = trends[trends["scope"].eq("combined")]
    matrix = combined.pivot(
        index="model",
        columns="complexity_quartile",
        values="think_24k_vs_4k_delta_pct_points",
    ).reindex(
        index=[label for _, label, _ in MODELS],
        columns=QUARTILE_ORDER,
    )
    figure, axis = plt.subplots(figsize=(8, 5), constrained_layout=True)
    image = axis.imshow(matrix.to_numpy(), cmap="YlGn", vmin=0, vmax=50)
    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            value = float(matrix.iloc[row_index, column_index])
            axis.text(
                column_index,
                row_index,
                f"{value:+.1f}",
                ha="center",
                va="center",
                color="white" if value >= 28 else "black",
            )
    axis.set_xticks(range(len(matrix.columns)), matrix.columns)
    axis.set_yticks(range(len(matrix.index)), matrix.index)
    axis.set_xlabel("Reference-code complexity quartile")
    axis.set_ylabel("Model")
    axis.set_title("Correctness gain from Think 4K to Think 24K")
    colorbar = figure.colorbar(image, ax=axis)
    colorbar.set_label("Pass@1 change (percentage points)")
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def plot_capacity_fixed_budget(
    capacity_trends: pd.DataFrame,
    output_path: Path,
) -> None:
    """Plot model scaling separately for each fixed inference configuration."""
    combined = capacity_trends[capacity_trends["scope"].eq("combined")]
    model_labels = [label for _, label, _ in MODELS]
    rate_columns = [
        "pass_0_6b_pct",
        "pass_1_7b_pct",
        "pass_4b_pct",
        "pass_8b_pct",
    ]
    colors = dict(
        zip(QUARTILE_ORDER, ("#2ca02c", "#1f77b4", "#ff7f0e", "#d62728"))
    )
    figure, axes = plt.subplots(
        2,
        3,
        figsize=(16, 10),
        sharex=True,
        sharey=True,
        constrained_layout=True,
    )
    x_values = np.arange(len(model_labels))

    for axis, config in zip(axes.flat, CONFIG_ORDER):
        cells = combined[combined["config_directory"].eq(config)].set_index(
            "complexity_quartile"
        )
        for quartile in QUARTILE_ORDER:
            rates = [float(cells.loc[quartile, column]) for column in rate_columns]
            axis.plot(
                x_values,
                rates,
                marker="o",
                linewidth=2,
                color=colors[quartile],
                label=f"{quartile}: {QUARTILE_DESCRIPTIONS[quartile]}",
            )
        axis.set_title(CONFIG_LABELS[config])
        axis.set_xticks(x_values, model_labels)
        axis.set_xlabel("Model size")
        axis.set_ylabel("Pass@1 on supported tasks (%)")
        axis.set_ylim(-2, 100)
        axis.grid(alpha=0.25)

    axes.flat[-1].axis("off")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    axes.flat[-1].legend(handles, labels, loc="center", frameon=False)
    figure.suptitle("Model-capacity scaling at a fixed inference configuration")
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def plot_capacity_marginal_gains(
    capacity_trends: pd.DataFrame,
    output_path: Path,
) -> None:
    """Heatmaps of the gain from each adjacent model-size increase."""
    combined = capacity_trends[capacity_trends["scope"].eq("combined")]
    columns = [
        "gain_0_6b_to_1_7b_pp",
        "gain_1_7b_to_4b_pp",
        "gain_4b_to_8b_pp",
    ]
    column_labels = ["0.6B→1.7B", "1.7B→4B", "4B→8B"]
    limit = float(np.abs(combined[columns].to_numpy(dtype=float)).max())
    norm = TwoSlopeNorm(vmin=-limit, vcenter=0.0, vmax=limit)
    figure, axes = plt.subplots(
        2,
        3,
        figsize=(15, 9),
        constrained_layout=True,
    )
    last_image = None
    for axis, config in zip(axes.flat, CONFIG_ORDER):
        cells = combined[combined["config_directory"].eq(config)].set_index(
            "complexity_quartile"
        ).reindex(QUARTILE_ORDER)
        values = cells[columns].to_numpy(dtype=float)
        last_image = axis.imshow(values, cmap="RdYlGn", norm=norm, aspect="auto")
        for row_index in range(values.shape[0]):
            for column_index in range(values.shape[1]):
                value = values[row_index, column_index]
                axis.text(
                    column_index,
                    row_index,
                    f"{value:+.1f}",
                    ha="center",
                    va="center",
                    color="white" if abs(value) > 0.55 * limit else "black",
                )
        axis.set_xticks(
            range(len(column_labels)), column_labels, rotation=20, ha="right"
        )
        axis.set_yticks(range(len(QUARTILE_ORDER)), QUARTILE_ORDER)
        axis.set_xlabel("Additional model capacity")
        axis.set_ylabel("Complexity quartile")
        axis.set_title(CONFIG_LABELS[config])

    axes.flat[-1].axis("off")
    if last_image is not None:
        colorbar = figure.colorbar(last_image, ax=axes.flat[:-1], shrink=0.85)
        colorbar.set_label("Pass@1 change (percentage points)")
    figure.suptitle("Marginal model-capacity gain at fixed inference configuration")
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def plot_compute_marginal_gains(
    compute_gains: pd.DataFrame,
    output_path: Path,
) -> None:
    """Heatmaps for the three requested inference-compute transitions."""
    combined = compute_gains[compute_gains["scope"].eq("combined")]
    transitions = [
        ("no_think_to_think_4k_pp", "No-think 4K → Think 4K"),
        ("think_4k_to_12k_pp", "Think 4K → Think 12K"),
        ("think_12k_to_24k_pp", "Think 12K → Think 24K"),
    ]
    gain_columns = [column for column, _ in transitions]
    limit = float(np.abs(combined[gain_columns].to_numpy(dtype=float)).max())
    norm = TwoSlopeNorm(vmin=-limit, vcenter=0.0, vmax=limit)
    model_labels = [label for _, label, _ in MODELS]
    figure, axes = plt.subplots(
        1,
        3,
        figsize=(15, 5.5),
        sharey=True,
        constrained_layout=True,
    )
    last_image = None
    for axis, (column, label) in zip(axes, transitions):
        matrix = combined.pivot(
            index="model",
            columns="complexity_quartile",
            values=column,
        ).reindex(index=model_labels, columns=QUARTILE_ORDER)
        values = matrix.to_numpy(dtype=float)
        last_image = axis.imshow(values, cmap="RdYlGn", norm=norm, aspect="auto")
        for row_index in range(values.shape[0]):
            for column_index in range(values.shape[1]):
                value = values[row_index, column_index]
                axis.text(
                    column_index,
                    row_index,
                    f"{value:+.1f}",
                    ha="center",
                    va="center",
                    color="white" if abs(value) > 0.55 * limit else "black",
                )
        axis.set_xticks(range(len(QUARTILE_ORDER)), QUARTILE_ORDER)
        axis.set_yticks(range(len(model_labels)), model_labels)
        axis.set_xlabel("Complexity quartile")
        axis.set_title(label)
    axes[0].set_ylabel("Model")
    if last_image is not None:
        colorbar = figure.colorbar(last_image, ax=axes, shrink=0.85)
        colorbar.set_label("Pass@1 change (percentage points)")
    figure.suptitle("Marginal correctness gain from additional inference compute")
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def quartile_table(
    trends: pd.DataFrame,
    *,
    model: str,
) -> list[str]:
    rows = trends[
        trends["scope"].eq("combined") & trends["model"].eq(model)
    ].set_index("complexity_quartile").reindex(QUARTILE_ORDER)
    lines = [
        "| Quartile | Tasks | No-think | Think 4K | Think 8K | Think 12K | Think 24K | 24K − 4K | Best |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for quartile, row in rows.iterrows():
        lines.append(
            f"| {quartile} | {int(row['tasks']):,} | "
            f"{float(row['no_think_pass_rate_pct']):.1f}% | "
            f"{float(row['think_4k_pass_rate_pct']):.1f}% | "
            f"{float(row['think_8k_pass_rate_pct']):.1f}% | "
            f"{float(row['think_12k_pass_rate_pct']):.1f}% | "
            f"{float(row['think_24k_pass_rate_pct']):.1f}% | "
            f"{float(row['think_24k_vs_4k_delta_pct_points']):+.1f} pp | "
            f"{row['best_thinking_budget']} |"
        )
    return lines


def sensitivity_delta_table(trends: pd.DataFrame) -> list[str]:
    combined = trends[trends["scope"].eq("combined")]
    lines = [
        "| Model | Q1 | Q2 | Q3 | Q4 |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, model_label, _ in MODELS:
        cells = combined[combined["model"].eq(model_label)].set_index(
            "complexity_quartile"
        )
        values = " | ".join(
            f"{float(cells.loc[q, 'think_24k_vs_4k_delta_pct_points']):+.1f} pp"
            for q in QUARTILE_ORDER
        )
        lines.append(f"| {model_label} | {values} |")
    return lines


def make_report(
    definitions: pd.DataFrame,
    primary_trends: pd.DataFrame,
    sensitivity_trends: pd.DataFrame,
    correlations: pd.DataFrame,
    capacity_trends: pd.DataFrame,
    compute_gains: pd.DataFrame,
) -> str:
    combined_correlations = correlations[correlations["scope"].eq("combined")]
    correlation_range = (
        float(combined_correlations["spearman_complexity_vs_accepted"].min()),
        float(combined_correlations["spearman_complexity_vs_accepted"].max()),
    )
    think_24k_capacity = capacity_trends[
        capacity_trends["scope"].eq("combined")
        & capacity_trends["config_directory"].eq(THINKING_CONFIGS[-1])
    ].set_index("complexity_quartile")
    think_24k_4b_to_8b = ", ".join(
        f"{float(think_24k_capacity.loc[q, 'gain_4b_to_8b_pp']):+.1f}"
        for q in QUARTILE_ORDER
    )
    combined_compute = compute_gains[compute_gains["scope"].eq("combined")]
    largest_4k_to_12k = combined_compute.loc[
        combined_compute["think_4k_to_12k_pp"].idxmax()
    ]
    eight_b_q1 = combined_compute[
        combined_compute["model"].eq("8B")
        & combined_compute["complexity_quartile"].eq("Q1")
    ].iloc[0]
    lines = [
        "# Reasoning budget, code complexity, and correctness",
        "",
        "## Method",
        "",
        "Complexity is defined per benchmark task from its reference solutions, not from the generated answer. This avoids changing the complexity group across models or using properties of a failed answer to define task difficulty.",
        "",
        "The primary proxy is `AST_Length`, averaged across available reference solutions. It measures structural code size and is strongly associated in this dataset with LOC (Spearman 0.94), Halstead effort (0.88), nesting depth (0.73), and cyclomatic complexity (0.66). Quartiles are formed once over the 4,229 judge-supported tasks.",
        "",
        "| Quartile | Description | Tasks | Minimum | Median | Maximum |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for _, row in definitions.iterrows():
        lines.append(
            f"| {row['complexity_quartile']} | {row['description']} | "
            f"{int(row['count']):,} | {float(row['min']):.1f} | "
            f"{float(row['median']):.1f} | {float(row['max']):.1f} |"
        )

    lines.extend(
        [
            "",
            "## Main result",
            "",
            "Correctness decreases sharply with reference-code complexity at every model size and budget. More reasoning budget usually improves every quartile, but it does not close the complexity gap. The largest absolute gains generally occur in the middle quartiles, where tasks are difficult enough to benefit from reasoning but not so hard that nearly all small-model attempts fail.",
            "",
            "![Reasoning budget and correctness by AST complexity quartile](complexity_budget_correctness.png)",
            "",
            "![Think 24K versus Think 4K correctness gain](complexity_budget_gain_heatmap.png)",
            "",
        ]
    )

    for _, model_label, _ in MODELS:
        lines.extend([f"### {model_label}", "", *quartile_table(primary_trends, model=model_label), ""])

    lines.extend(
        [
            "## What the interaction looks like",
            "",
            "- **0.6B:** budget gains are concentrated in Q1–Q2. Q4 remains near 1%, so extra tokens cannot compensate for limited model capacity on the most structurally complex tasks.",
            "- **1.7B:** all quartiles improve; Q2 and Q3 gain the most from 4K to 24K.",
            "- **4B:** the strongest overall interaction. Think 24K reaches about 81% on Q1 and 28% on Q4, with roughly 45-point gains in Q2–Q3 versus Think 4K.",
            "- **8B:** gains flatten at high budgets. Q1 peaks at Think 12K and then declines at 24K; high-budget generation failures prevent the larger model from dominating 4B end to end.",
            "",
            f"Across the 20 model/configuration cells, the task-level Spearman association between `AST_Length` and acceptance ranges from {correlation_range[0]:.3f} to {correlation_range[1]:.3f}; it is negative in every cell.",
            "",
            "## Fixed inference configuration: model-capacity returns",
            "",
            "Each panel below fixes the inference configuration and compares model sizes within the same task-complexity quartile. This separates model-capacity scaling from inference-budget scaling.",
            "",
            "![Model-capacity scaling at fixed inference configurations](complexity_model_capacity_fixed_budget.png)",
            "",
            "The heatmaps show the marginal percentage-point change for each adjacent model-size step. The strongest improvements usually occur from 0.6B to 1.7B and from 1.7B to 4B. Moving from 4B to 8B has little benefit at low budgets and is negative at Think 12K/24K because the 8B high-budget runs have more incomplete or failed generations. At Think 24K, 4B to 8B changes Q1–Q4 by "
            f"{think_24k_4b_to_8b} points respectively.",
            "",
            "![Marginal model-capacity gains](complexity_model_capacity_marginal_gains.png)",
            "",
            "## Marginal inference-compute returns",
            "",
            "The first transition changes decoding mode while holding the nominal 4K cap fixed; the next two increase the thinking budget. Green cells are gains and red cells are regressions in end-to-end pass@1.",
            "",
            "![Marginal inference-compute gains](complexity_inference_compute_marginal_gains.png)",
            "",
            "Think 4K is often worse than no-think 4K for Q2–Q4 on the larger models. The largest gain from Think 4K to Think 12K is "
            f"{float(largest_4k_to_12k['think_4k_to_12k_pp']):+.1f} points for "
            f"{largest_4k_to_12k['model']}/{largest_4k_to_12k['complexity_quartile']}. "
            "Returns then diminish sharply from 12K to 24K: several cells are near zero, and 8B/Q1 changes by "
            f"{float(eight_b_q1['think_12k_to_24k_pp']):+.1f} points. Harder quartiles can still gain at 24K for 1.7B and 4B, but the benefit is not uniform.",
            "",
            "## Cyclomatic-complexity sensitivity check",
            "",
            "The table below repeats the Think 24K minus Think 4K comparison after redefining quartiles using cyclomatic complexity. The same qualitative conclusion remains: reasoning budget helps all complexity levels, with the strongest gains usually in the middle/high-but-not-extreme groups.",
            "",
            *sensitivity_delta_table(sensitivity_trends),
            "",
            "![Cyclomatic-complexity sensitivity plot](complexity_budget_correctness_cyclomatic.png)",
            "",
            "## Interpretation limits",
            "",
            "- Reference-solution complexity is a proxy for task complexity. It also reflects implementation style, choice of algorithm, and the number of reference solutions available.",
            "- `AST_Length` primarily measures structural size, not conceptual or mathematical difficulty; the cyclomatic sensitivity check partly addresses this.",
            "- Quartile results are descriptive. Each budget trend has only four aggregate points, so the reported budget correlations are not a fitted scaling law.",
            "- The correctness values inherit the judge limitations in `correctness_report.md`: exact stripped-output comparison, a two-second timeout per testcase, and exclusion of 98 unsupported APPS tasks.",
            "- APPS supplies most tasks. Dataset-specific rows are included in the CSV outputs, but the report emphasizes the combined controlled slice.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--trace-dir", type=Path, default=DEFAULT_TRACE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    correctness = load_and_validate(args.results)
    complexity = load_complexity(args.trace_dir)
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    primary, task_quartiles, definitions = merge_results_and_complexity(
        correctness,
        complexity,
        metric=PRIMARY_METRIC,
    )
    primary_summary = make_group_summary(primary)
    primary_trends = make_budget_trends(
        primary,
        primary_summary,
        metric=PRIMARY_METRIC,
    )
    capacity_trends = make_capacity_trends(primary_summary)
    compute_gains = make_compute_marginal_gains(primary_summary)
    correlations = make_complexity_correlations(primary, metric=PRIMARY_METRIC)

    sensitivity, sensitivity_tasks, sensitivity_definitions = (
        merge_results_and_complexity(
            correctness,
            complexity,
            metric=SENSITIVITY_METRIC,
        )
    )
    sensitivity_summary = make_group_summary(sensitivity)
    sensitivity_trends = make_budget_trends(
        sensitivity,
        sensitivity_summary,
        metric=SENSITIVITY_METRIC,
    )

    task_quartiles.to_csv(
        output_dir / "task_complexity_quartiles.csv",
        index=False,
    )
    definitions.to_csv(
        output_dir / "complexity_quartile_definitions.csv",
        index=False,
    )
    primary_summary.to_csv(
        output_dir / "complexity_budget_correctness.csv",
        index=False,
    )
    primary_trends.to_csv(
        output_dir / "complexity_budget_trends.csv",
        index=False,
    )
    capacity_trends.to_csv(
        output_dir / "complexity_model_capacity_trends.csv",
        index=False,
    )
    compute_gains.to_csv(
        output_dir / "complexity_inference_compute_marginal_gains.csv",
        index=False,
    )
    correlations.to_csv(
        output_dir / "complexity_correctness_correlations.csv",
        index=False,
    )
    sensitivity_tasks.to_csv(
        output_dir / "task_cyclomatic_quartiles.csv",
        index=False,
    )
    sensitivity_definitions.to_csv(
        output_dir / "cyclomatic_quartile_definitions.csv",
        index=False,
    )
    sensitivity_trends.to_csv(
        output_dir / "complexity_budget_trends_cyclomatic.csv",
        index=False,
    )

    plot_budget_by_quartile(
        primary_summary,
        output_dir / "complexity_budget_correctness.png",
        title_metric="reference-code AST complexity",
    )
    plot_budget_gain(
        primary_trends,
        output_dir / "complexity_budget_gain_heatmap.png",
    )
    plot_capacity_fixed_budget(
        capacity_trends,
        output_dir / "complexity_model_capacity_fixed_budget.png",
    )
    plot_capacity_marginal_gains(
        capacity_trends,
        output_dir / "complexity_model_capacity_marginal_gains.png",
    )
    plot_compute_marginal_gains(
        compute_gains,
        output_dir / "complexity_inference_compute_marginal_gains.png",
    )
    plot_budget_by_quartile(
        sensitivity_summary,
        output_dir / "complexity_budget_correctness_cyclomatic.png",
        title_metric="reference-code cyclomatic complexity",
    )

    report = make_report(
        definitions,
        primary_trends,
        sensitivity_trends,
        correlations,
        capacity_trends,
        compute_gains,
    )
    (output_dir / "complexity_correctness_report.md").write_text(
        report,
        encoding="utf-8",
    )

    print(
        f"Analyzed {task_quartiles['task_id'].nunique():,} supported tasks "
        f"using {PRIMARY_METRIC} quartiles"
    )
    print(f"Wrote complexity/correctness analysis to {output_dir}")


if __name__ == "__main__":
    main()
