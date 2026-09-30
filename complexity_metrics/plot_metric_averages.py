from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import fmean


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACE_DIR = PROJECT_ROOT / "complexity_metrics" / "fair_traces"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "complexity_metrics" / "outputs"

DATASETS = (
    ("HumanEval", "humaneval_test.jsonl"),
    ("MBPP", "mbpp_test.jsonl"),
    ("APPS", "apps_test.jsonl"),
    ("LCB", "lcb_test.jsonl"),
)

# Keep the metric presentation stable instead of relying on JSON key order.
METRICS = (
    "AST_Length",
    "Max_Nesting_Depth",
    "Number_of_Calls",
    "Number_of_Vars",
    "cyclomatic",
    "maintainability",
    "halstead_volume",
    "halstead_difficulty",
    "halstead_effort",
    "halstead_bugs",
    "loc",
    "lloc",
    "sloc",
    "comments",
    "blank",
)


def load_metric_means(trace_dir: Path) -> dict[str, dict[str, float]]:
    means: dict[str, dict[str, float]] = {}
    for dataset, filename in DATASETS:
        rows = []
        with (trace_dir / filename).open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))

        if not rows:
            raise ValueError(f"No trace rows found in {trace_dir / filename}")

        missing = [metric for metric in METRICS if any(metric not in row for row in rows)]
        if missing:
            raise ValueError(f"Missing metrics in {filename}: {sorted(set(missing))}")

        means[dataset] = {
            metric: fmean(float(row[metric]) for row in rows) for metric in METRICS
        }
    return means


def write_csv(path: Path, means: dict[str, dict[str, float]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("metric", *(dataset for dataset, _ in DATASETS)))
        for metric in METRICS:
            writer.writerow((metric, *(means[dataset][metric] for dataset, _ in DATASETS)))


def write_plot(path: Path, means: dict[str, dict[str, float]]) -> None:
    import matplotlib.pyplot as plt

    colors = ("#4C78A8", "#F58518", "#54A24B", "#E45756")
    dataset_names = [dataset for dataset, _ in DATASETS]
    figure, axes = plt.subplots(5, 3, figsize=(15, 20), constrained_layout=True)

    for axis, metric in zip(axes.flat, METRICS):
        values = [means[dataset][metric] for dataset in dataset_names]
        bars = axis.bar(dataset_names, values, color=colors)
        axis.set_title(metric.replace("_", " "))
        axis.tick_params(axis="x", rotation=20)
        axis.grid(axis="y", alpha=0.25)
        axis.bar_label(bars, fmt="%.2g", padding=2, fontsize=8)

    figure.suptitle("Average trace metrics across the four datasets", fontsize=18)
    figure.savefig(path, dpi=200)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot task-weighted average trace metrics for HumanEval, MBPP, APPS, and LCB."
    )
    parser.add_argument("--trace-dir", type=Path, default=DEFAULT_TRACE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    means = load_metric_means(args.trace_dir)
    csv_path = args.output_dir / "trace_metric_dataset_means.csv"
    plot_path = args.output_dir / "trace_metric_dataset_means.png"
    write_csv(csv_path, means)
    write_plot(plot_path, means)
    print(f"Wrote {csv_path}")
    print(f"Wrote {plot_path}")


if __name__ == "__main__":
    main()
