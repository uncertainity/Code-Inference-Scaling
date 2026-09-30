#!/usr/bin/env python3
"""Analyze the complete APPS/LCB slice of the Qwen3 scaling experiment.

The script intentionally depends only on the Python standard library and
matplotlib.  It reads generation JSONL files in a streaming fashion, validates
that every model/configuration cell contains the same task IDs, and writes
tables, correlations, and plots to ``analysis/outputs``.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from statistics import fmean, median
from typing import Iterable, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_DIR = (
    PROJECT_ROOT / "generation" / "runs" / "vllm" / "scaling_law_001"
)
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


@dataclass(frozen=True)
class ModelSpec:
    directory: str
    label: str
    parameters_b: float


@dataclass(frozen=True)
class ConfigSpec:
    directory: str
    label: str
    thinking: bool
    max_tokens: int


MODELS = (
    ModelSpec("Qwen3-0.6B", "0.6B", 0.6),
    ModelSpec("Qwen3-1.7B", "1.7B", 1.7),
    ModelSpec("Qwen3-4B", "4B", 4.0),
    ModelSpec("Qwen3-8B", "8B", 8.0),
)

CONFIGS = (
    ConfigSpec("no_thinking_sampled_4k", "No-think 4K", False, 4096),
    ConfigSpec("thinking_4k_presence_1_0", "Think 4K", True, 4096),
    ConfigSpec("thinking_8k_presence_1_0", "Think 8K", True, 8192),
    ConfigSpec("thinking_12k_presence_1_0", "Think 12K", True, 12000),
    ConfigSpec("thinking_24k_presence_1_0", "Think 24K", True, 24000),
)

DEFAULT_DATASETS = ("apps", "lcb")
CORRELATION_ERROR_THRESHOLD_PCT = 1.0


@dataclass
class Accumulator:
    completion_tokens: list[float] = field(default_factory=list)
    task_ids: set[str] = field(default_factory=set)
    total: int = 0
    normal_stops: int = 0
    length_stops: int = 0
    final_answers: int = 0
    errors: int = 0
    missing_usage: int = 0

    def add(self, row: dict, *, thinking: bool, source: Path, line_number: int) -> None:
        task_id = str(row.get("task_id", ""))
        if not task_id:
            raise ValueError(f"Missing task_id in {source}:{line_number}")
        if task_id in self.task_ids:
            raise ValueError(f"Duplicate task_id {task_id!r} in {source}")
        self.task_ids.add(task_id)
        self.total += 1

        finish_reason = row.get("finish_reason")
        self.normal_stops += finish_reason == "stop"
        self.length_stops += finish_reason == "length"
        self.errors += finish_reason == "error" or bool(row.get("error"))

        prediction = row.get("prediction") or ""
        if thinking:
            self.final_answers += "</think>" in prediction and bool(
                prediction.rsplit("</think>", 1)[1].strip()
            )
        else:
            self.final_answers += bool(prediction.strip())

        usage = row.get("usage") or {}
        tokens = usage.get("completion_tokens")
        if isinstance(tokens, (int, float)) and not isinstance(tokens, bool):
            self.completion_tokens.append(float(tokens))
        else:
            self.missing_usage += 1

    def extend(self, other: "Accumulator") -> None:
        overlap = self.task_ids & other.task_ids
        if overlap:
            example = sorted(overlap)[0]
            raise ValueError(f"Duplicate task ID while pooling datasets: {example!r}")
        self.completion_tokens.extend(other.completion_tokens)
        self.task_ids.update(other.task_ids)
        self.total += other.total
        self.normal_stops += other.normal_stops
        self.length_stops += other.length_stops
        self.final_answers += other.final_answers
        self.errors += other.errors
        self.missing_usage += other.missing_usage


def percentile(values: Sequence[float], quantile: float) -> float:
    if not values:
        return math.nan
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def percent(numerator: int, denominator: int) -> float:
    return 100.0 * numerator / denominator if denominator else math.nan


def summarize(
    accumulator: Accumulator,
    *,
    scope: str,
    model: ModelSpec,
    config: ConfigSpec,
) -> dict[str, object]:
    tokens = accumulator.completion_tokens
    return {
        "scope": scope,
        "model": model.label,
        "model_directory": model.directory,
        "model_parameters_b": model.parameters_b,
        "config": config.label,
        "config_directory": config.directory,
        "thinking": config.thinking,
        "max_tokens": config.max_tokens,
        "rows": accumulator.total,
        "rows_with_token_usage": len(tokens),
        "missing_token_usage": accumulator.missing_usage,
        "mean_completion_tokens": fmean(tokens) if tokens else math.nan,
        "median_completion_tokens": median(tokens) if tokens else math.nan,
        "p95_completion_tokens": percentile(tokens, 0.95),
        "normal_stop_rate_pct": percent(accumulator.normal_stops, accumulator.total),
        "length_stop_rate_pct": percent(accumulator.length_stops, accumulator.total),
        "final_answer_rate_pct": percent(accumulator.final_answers, accumulator.total),
        "error_rate_pct": percent(accumulator.errors, accumulator.total),
    }


def read_file(path: Path, *, thinking: bool) -> Accumulator:
    accumulator = Accumulator()
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line.strip():
                accumulator.add(
                    json.loads(line),
                    thinking=thinking,
                    source=path,
                    line_number=line_number,
                )
    return accumulator


def collect_summaries(
    run_dir: Path, datasets: Sequence[str]
) -> tuple[list[dict[str, object]], dict[tuple[str, str], dict[str, object]], int]:
    rows: list[dict[str, object]] = []
    combined: dict[tuple[str, str], dict[str, object]] = {}
    reference_task_ids: dict[str, set[str]] = {}

    for model in MODELS:
        for config in CONFIGS:
            pooled = Accumulator()
            for dataset in datasets:
                path = (
                    run_dir
                    / "models"
                    / model.directory
                    / config.directory
                    / f"{dataset}_test_generations.jsonl"
                )
                if not path.is_file():
                    raise FileNotFoundError(
                        f"Missing required generation file: {path}\n"
                        "Use only datasets with complete coverage or finish the missing run."
                    )
                accumulator = read_file(path, thinking=config.thinking)

                reference = reference_task_ids.setdefault(dataset, accumulator.task_ids)
                if accumulator.task_ids != reference:
                    missing = len(reference - accumulator.task_ids)
                    extra = len(accumulator.task_ids - reference)
                    raise ValueError(
                        f"Task coverage mismatch in {path}: missing={missing}, extra={extra}"
                    )

                rows.append(
                    summarize(
                        accumulator,
                        scope=dataset,
                        model=model,
                        config=config,
                    )
                )
                pooled.extend(accumulator)

            pooled_summary = summarize(
                pooled,
                scope="combined",
                model=model,
                config=config,
            )
            rows.append(pooled_summary)
            combined[(model.label, config.label)] = pooled_summary

    tasks_per_cell = sum(len(task_ids) for task_ids in reference_task_ids.values())
    return rows, combined, tasks_per_cell


SUMMARY_FIELDS = (
    "scope",
    "model",
    "model_directory",
    "model_parameters_b",
    "config",
    "config_directory",
    "thinking",
    "max_tokens",
    "rows",
    "rows_with_token_usage",
    "missing_token_usage",
    "mean_completion_tokens",
    "median_completion_tokens",
    "p95_completion_tokens",
    "normal_stop_rate_pct",
    "length_stop_rate_pct",
    "final_answer_rate_pct",
    "error_rate_pct",
)


def write_dict_csv(path: Path, rows: Iterable[dict[str, object]], fields: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def metric_matrix(
    combined: dict[tuple[str, str], dict[str, object]], metric: str
) -> list[list[float]]:
    return [
        [float(combined[(model.label, config.label)][metric]) for config in CONFIGS]
        for model in MODELS
    ]


def write_matrix_csv(path: Path, matrix: Sequence[Sequence[float]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("Model", *(config.label for config in CONFIGS)))
        for model, values in zip(MODELS, matrix):
            writer.writerow((model.label, *(f"{value:.6f}" for value in values)))


def pearson_r(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return math.nan
    x_mean = fmean(xs)
    y_mean = fmean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    x_ss = sum((x - x_mean) ** 2 for x in xs)
    y_ss = sum((y - y_mean) ** 2 for y in ys)
    denominator = math.sqrt(x_ss * y_ss)
    return numerator / denominator if denominator else math.nan


CORRELATION_METRICS = (
    "mean_completion_tokens",
    "median_completion_tokens",
    "p95_completion_tokens",
    "normal_stop_rate_pct",
    "length_stop_rate_pct",
    "final_answer_rate_pct",
    "error_rate_pct",
)


def model_size_correlations(
    combined: dict[tuple[str, str], dict[str, object]]
) -> list[dict[str, object]]:
    log_model_sizes = [math.log10(model.parameters_b) for model in MODELS]
    rows = []
    for config in CONFIGS:
        error_rates = [
            float(combined[(model.label, config.label)]["error_rate_pct"])
            for model in MODELS
        ]
        row: dict[str, object] = {
            "config": config.label,
            "max_error_rate_pct": max(error_rates),
            "confounded_by_errors": max(error_rates) > CORRELATION_ERROR_THRESHOLD_PCT,
        }
        for metric in CORRELATION_METRICS:
            values = [float(combined[(model.label, config.label)][metric]) for model in MODELS]
            row[f"{metric}_pearson_r"] = pearson_r(log_model_sizes, values)
        rows.append(row)
    return rows


def budget_correlations(
    combined: dict[tuple[str, str], dict[str, object]]
) -> list[dict[str, object]]:
    thinking_configs = [config for config in CONFIGS if config.thinking]
    log_budgets = [math.log2(config.max_tokens) for config in thinking_configs]
    rows = []
    for model in MODELS:
        error_rates = [
            float(combined[(model.label, config.label)]["error_rate_pct"])
            for config in thinking_configs
        ]
        row: dict[str, object] = {
            "model": model.label,
            "max_error_rate_pct": max(error_rates),
            "confounded_by_errors": max(error_rates) > CORRELATION_ERROR_THRESHOLD_PCT,
        }
        for metric in CORRELATION_METRICS:
            values = [
                float(combined[(model.label, config.label)][metric])
                for config in thinking_configs
            ]
            row[f"{metric}_pearson_r"] = pearson_r(log_budgets, values)
        rows.append(row)
    return rows


def write_heatmap(
    path: Path,
    matrix: Sequence[Sequence[float]],
    *,
    title: str,
    colorbar_label: str,
    annotation_format: str,
) -> None:
    import matplotlib.pyplot as plt

    figure, axis = plt.subplots(figsize=(10.5, 5.4), constrained_layout=True)
    image = axis.imshow(matrix, cmap="viridis", aspect="auto")
    axis.set_xticks(range(len(CONFIGS)), [config.label for config in CONFIGS])
    axis.set_yticks(range(len(MODELS)), [model.label for model in MODELS])
    axis.set_xlabel("Inference configuration")
    axis.set_ylabel("Qwen3 model size")
    axis.set_title(title)
    plt.setp(axis.get_xticklabels(), rotation=25, ha="right", rotation_mode="anchor")

    flat_values = [value for row in matrix for value in row]
    threshold = (min(flat_values) + max(flat_values)) / 2.0
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            color = "black" if value > threshold else "white"
            axis.text(
                column_index,
                row_index,
                format(value, annotation_format),
                ha="center",
                va="center",
                color=color,
                fontsize=9,
                fontweight="bold",
            )

    colorbar = figure.colorbar(image, ax=axis, shrink=0.88)
    colorbar.set_label(colorbar_label)
    figure.savefig(path, dpi=200)
    plt.close(figure)


def write_relationship_plot(
    path: Path, combined: dict[tuple[str, str], dict[str, object]]
) -> None:
    import matplotlib.pyplot as plt

    panels = (
        ("mean_completion_tokens", "Mean completion tokens"),
        ("median_completion_tokens", "Median completion tokens"),
        ("normal_stop_rate_pct", "Normal-stop rate (%)"),
        ("final_answer_rate_pct", "Final-answer rate (%)"),
        ("length_stop_rate_pct", "Token-limit stop rate (%)"),
        ("error_rate_pct", "Request error rate (%)"),
    )
    colors = plt.get_cmap("tab10").colors
    figure, axes = plt.subplots(2, 3, figsize=(19, 10))
    x_values = [model.parameters_b for model in MODELS]

    for axis, (metric, title) in zip(axes.flat, panels):
        for index, config in enumerate(CONFIGS):
            y_values = [
                float(combined[(model.label, config.label)][metric]) for model in MODELS
            ]
            axis.plot(
                x_values,
                y_values,
                marker="o",
                linewidth=2,
                label=config.label,
                color=colors[index],
            )
        axis.set_xscale("log")
        axis.set_xticks(x_values, [model.label for model in MODELS])
        axis.set_xlabel("Model parameters")
        axis.set_ylabel(title)
        axis.set_title(title)
        axis.grid(True, alpha=0.25)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.955),
        ncols=len(CONFIGS),
    )
    figure.suptitle(
        "Qwen3 generation behavior on the complete APPS + LCB slice",
        fontsize=16,
        y=0.995,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.90))
    figure.savefig(path, dpi=200)
    plt.close(figure)


def markdown_matrix(
    matrix: Sequence[Sequence[float]], *, annotation_format: str
) -> list[str]:
    lines = [
        "| Model | " + " | ".join(config.label for config in CONFIGS) + " |",
        "|---|" + "---:|" * len(CONFIGS),
    ]
    for model, values in zip(MODELS, matrix):
        formatted = [format(value, annotation_format) for value in values]
        lines.append(f"| {model.label} | " + " | ".join(formatted) + " |")
    return lines


def format_r(value: object) -> str:
    number = float(value)
    return "n/a" if math.isnan(number) else f"{number:+.3f}"


def report_correlation(row: dict[str, object], metric: str) -> str:
    if row["confounded_by_errors"]:
        return "confounded"
    return format_r(row[f"{metric}_pearson_r"])


def write_report(
    path: Path,
    *,
    run_dir: Path,
    datasets: Sequence[str],
    tasks_per_cell: int,
    combined: dict[tuple[str, str], dict[str, object]],
    model_correlations: Sequence[dict[str, object]],
    budget_correlations_rows: Sequence[dict[str, object]],
) -> None:
    mean_matrix = metric_matrix(combined, "mean_completion_tokens")
    median_matrix = metric_matrix(combined, "median_completion_tokens")
    normal_matrix = metric_matrix(combined, "normal_stop_rate_pct")
    final_matrix = metric_matrix(combined, "final_answer_rate_pct")
    error_matrix = metric_matrix(combined, "error_rate_pct")
    total_generations = tasks_per_cell * len(MODELS) * len(CONFIGS)

    lines = [
        "# Qwen3 scaling analysis",
        "",
        f"Source run: `{run_dir}`",
        "",
        f"Controlled datasets: {', '.join(dataset.upper() for dataset in datasets)}.",
        f"Every matrix cell contains the same {tasks_per_cell:,} tasks; the analysis covers "
        f"{total_generations:,} generations across {len(MODELS)} models and {len(CONFIGS)} configurations.",
        "",
        "The tables describe generation behavior, not program correctness. No pass/fail evaluation is present in these generation files.",
        "",
        "## Mean completion tokens",
        "",
        *markdown_matrix(mean_matrix, annotation_format=",.1f"),
        "",
        "Means and medians use rows containing token usage. Request failures have no token usage and are excluded, so inspect the error-rate table before interpreting apparent length reductions.",
        "",
        "![Mean completion-token heatmap](mean_completion_tokens_heatmap.png)",
        "",
        "## Median completion tokens",
        "",
        *markdown_matrix(median_matrix, annotation_format=",.1f"),
        "",
        "## Normal-stop rate",
        "",
        *markdown_matrix(normal_matrix, annotation_format=".2f"),
        "",
        "Values are percentages. A normal stop has `finish_reason == \"stop\"`.",
        "",
        "## Final-answer rate",
        "",
        *markdown_matrix(final_matrix, annotation_format=".2f"),
        "",
        "For thinking configurations, a final answer requires a closed `</think>` block followed by non-empty text. For the no-thinking baseline, it means a non-empty response.",
        "",
        "## Request error rate",
        "",
        *markdown_matrix(error_matrix, annotation_format=".2f"),
        "",
        "Values are percentages. Errors in this run are HTTP-client failures recorded by the generator, principally `ReadTimeout`; they must not be interpreted as short successful generations.",
        "",
        "![Request-error heatmap](error_rate_heatmap.png)",
        "",
        "![Scaling relationship plots](scaling_relationships.png)",
        "",
        "## Descriptive correlations",
        "",
        "Pearson correlations are descriptive checks based on only four model sizes or four thinking budgets. They should not be treated as fitted scaling laws. A series is marked `confounded` when any included cell has more than 1% request errors.",
        "",
        "### Model size",
        "",
        "Correlation against log10(model parameters):",
        "",
        "| Configuration | Mean tokens r | Median tokens r | Normal-stop r | Final-answer r | Max error rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in model_correlations:
        lines.append(
            f"| {row['config']} | {report_correlation(row, 'mean_completion_tokens')} | "
            f"{report_correlation(row, 'median_completion_tokens')} | "
            f"{report_correlation(row, 'normal_stop_rate_pct')} | "
            f"{report_correlation(row, 'final_answer_rate_pct')} | "
            f"{float(row['max_error_rate_pct']):.2f}% |"
        )

    lines += [
        "",
        "### Thinking budget",
        "",
        "Correlation against log2(maximum thinking tokens), excluding the no-thinking baseline:",
        "",
        "| Model | Mean tokens r | Median tokens r | Normal-stop r | Final-answer r | Max error rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in budget_correlations_rows:
        lines.append(
            f"| {row['model']} | {report_correlation(row, 'mean_completion_tokens')} | "
            f"{report_correlation(row, 'median_completion_tokens')} | "
            f"{report_correlation(row, 'normal_stop_rate_pct')} | "
            f"{report_correlation(row, 'final_answer_rate_pct')} | "
            f"{float(row['max_error_rate_pct']):.2f}% |"
        )

    lines += [
        "",
        "## Files",
        "",
        "- `summary.csv`: combined and per-dataset statistics.",
        "- `*_matrix.csv`: the exact values used in the tables and heatmap.",
        "- `model_size_correlations.csv`: correlations across model sizes.",
        "- `thinking_budget_correlations.csv`: correlations across thinking budgets.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build tables and plots for the Qwen3 model-size/thinking-budget matrix."
    )
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=list(DEFAULT_DATASETS),
        help="Dataset stems to pool (default: apps lcb).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_rows, combined, tasks_per_cell = collect_summaries(run_dir, args.datasets)
    write_dict_csv(output_dir / "summary.csv", summary_rows, SUMMARY_FIELDS)

    matrices = {
        "mean_completion_tokens": metric_matrix(combined, "mean_completion_tokens"),
        "median_completion_tokens": metric_matrix(combined, "median_completion_tokens"),
        "p95_completion_tokens": metric_matrix(combined, "p95_completion_tokens"),
        "normal_stop_rate_pct": metric_matrix(combined, "normal_stop_rate_pct"),
        "length_stop_rate_pct": metric_matrix(combined, "length_stop_rate_pct"),
        "final_answer_rate_pct": metric_matrix(combined, "final_answer_rate_pct"),
        "error_rate_pct": metric_matrix(combined, "error_rate_pct"),
    }
    for name, matrix in matrices.items():
        write_matrix_csv(output_dir / f"{name}_matrix.csv", matrix)

    model_correlations = model_size_correlations(combined)
    correlation_fields = ("config", "max_error_rate_pct", "confounded_by_errors") + tuple(
        f"{metric}_pearson_r" for metric in CORRELATION_METRICS
    )
    write_dict_csv(
        output_dir / "model_size_correlations.csv",
        model_correlations,
        correlation_fields,
    )

    budget_correlation_rows = budget_correlations(combined)
    budget_fields = ("model", "max_error_rate_pct", "confounded_by_errors") + tuple(
        f"{metric}_pearson_r" for metric in CORRELATION_METRICS
    )
    write_dict_csv(
        output_dir / "thinking_budget_correlations.csv",
        budget_correlation_rows,
        budget_fields,
    )

    write_heatmap(
        output_dir / "mean_completion_tokens_heatmap.png",
        matrices["mean_completion_tokens"],
        title="Mean completion tokens by model size and inference configuration",
        colorbar_label="Mean completion tokens",
        annotation_format=",.0f",
    )
    write_heatmap(
        output_dir / "error_rate_heatmap.png",
        matrices["error_rate_pct"],
        title="Request error rate by model size and inference configuration",
        colorbar_label="Request error rate (%)",
        annotation_format=".1f",
    )
    write_relationship_plot(output_dir / "scaling_relationships.png", combined)
    write_report(
        output_dir / "report.md",
        run_dir=run_dir,
        datasets=args.datasets,
        tasks_per_cell=tasks_per_cell,
        combined=combined,
        model_correlations=model_correlations,
        budget_correlations_rows=budget_correlation_rows,
    )

    print(f"Analyzed {tasks_per_cell:,} tasks in each of {len(MODELS) * len(CONFIGS)} cells")
    print(f"Wrote analysis to {output_dir}")


if __name__ == "__main__":
    main()
