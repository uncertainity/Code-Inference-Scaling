from __future__ import annotations

import argparse
import csv
import json
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from itertools import islice
from pathlib import Path
from typing import Any, Iterator

try:
    from .evaluator import evaluate_job
    from .normalizer import normalize_generation
except ImportError:  # Support `python test_harness/harness.py`.
    from evaluator import evaluate_job
    from normalizer import normalize_generation


HARNESS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = HARNESS_DIR.parent

# Benchmark questions and their correctness tests.
BENCHMARK_DATA_DIR = PROJECT_ROOT / "fair_data" / "data_jsonl"

# Model predictions produced by the full Qwen3 scaling run.
RUN_DIR = PROJECT_ROOT / "generation" / "runs" / "vllm" / "scaling_law_001"
GENERATIONS_DIR = RUN_DIR / "models"

# The isolated Python environment and compact correctness results belong to
# this harness rather than to the source datasets or generation artifacts.
VENV_DIR = HARNESS_DIR / ".venv"
JUDGE_PYTHON = VENV_DIR / "bin" / "python"
RESULTS_DIR = HARNESS_DIR / "results" / RUN_DIR.name

MODELS = [
    "Qwen3-0.6B",
    "Qwen3-1.7B",
    "Qwen3-4B",
    "Qwen3-8B",
]

CONFIGS = [
    ("no_thinking_sampled_4k", False),
    ("thinking_4k_presence_1_0", True),
    ("thinking_8k_presence_1_0", True),
    ("thinking_12k_presence_1_0", True),
    ("thinking_24k_presence_1_0", True),
]

DATASETS = [
    ("lcb", "lcb_test.jsonl", "lcb_test_generations.jsonl"),
    ("apps", "apps_test.jsonl", "apps_test_generations.jsonl"),
]

RESULT_FIELDS = [
    "task_id",
    "dataset",
    "model",
    "config",
    "thinking",
    "status",
    "tests_total",
    "tests_passed",
    "failed_test_index",
    "input",
    "expected",
    "actual",
    "stderr",
    "returncode",
    "error",
]


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield one decoded object at a time without loading the JSONL into memory."""
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path} at line {line_number}: {exc.msg}"
                ) from exc

            if not isinstance(row, dict):
                raise ValueError(
                    f"Expected a JSON object in {path} at line {line_number}"
                )

            yield row


def stream_dataset(
    benchmark_spec: Path,
    generation_specs: list[tuple[str, str, bool, Path]],
) -> Iterator[dict[str, Any]]:
    """Yield one benchmark task with its normalized model generations."""
    benchmark_rows = read_jsonl(benchmark_spec)
    generation_streams = [
        read_jsonl(path) for _, _, _, path in generation_specs
    ]

    for row_number, rows in enumerate(
        zip(benchmark_rows, *generation_streams, strict=True),
        start=1,
    ):
        benchmark_row = rows[0]
        generation_rows = rows[1:]

        if "task_id" not in benchmark_row:
            raise ValueError(
                f"Missing task_id in {benchmark_spec} at row {row_number}"
            )

        programs = []
        for spec, generation_row in zip(
            generation_specs,
            generation_rows,
            strict=True,
        ):
            model, config, thinking, path = spec
            if generation_row["task_id"] != benchmark_row["task_id"]:
                raise ValueError(
                    f"Task mismatch at row {row_number} for {model}/{config}: "
                    f"benchmark={benchmark_row['task_id']!r}, "
                    f"generation={generation_row.get('task_id')!r}, file={path}"
                )

            normalized = normalize_generation(
                task_id=generation_row["task_id"],
                prediction=generation_row.get("prediction") or "",
                thinking=thinking,
                finish_reason=generation_row.get("finish_reason"),
                error=generation_row.get("error"),
            )
            programs.append(
                {
                    "model": model,
                    "config": config,
                    "thinking": thinking,
                    "normalized": normalized,
                }
            )

        yield {
            "task_id": benchmark_row["task_id"],
            "dataset": benchmark_row.get("dataset"),
            "test_type": benchmark_row.get("test_type"),
            "tests": benchmark_row.get("tests"),
            "programs": programs,
        }


def main_process() -> Iterator[dict[str, Any]]:
    for dataset_name, benchmark_filename, generation_filename in DATASETS:
        benchmark_path = BENCHMARK_DATA_DIR / benchmark_filename
        generation_specs: list[tuple[str, str, bool, Path]] = []
        if not benchmark_path.is_file():
            raise FileNotFoundError(benchmark_path)

        for model in MODELS:
            for config, thinking in CONFIGS:
                generation_path = (
                    GENERATIONS_DIR / model / config / generation_filename
                )

                if not generation_path.is_file():
                    raise FileNotFoundError(generation_path)
                generation_specs.append(
                    (model, config, thinking, generation_path)
                )

        if len(generation_specs) != len(MODELS) * len(CONFIGS):
            raise ValueError(
                f"Expected 20 generation files for {dataset_name}, "
                f"found {len(generation_specs)}"
            )

        yield from stream_dataset(benchmark_path, generation_specs)


def worker_error_results(
    job: dict[str, Any],
    exc: Exception,
) -> list[dict[str, Any]]:
    """Represent an unexpected worker exception without losing the whole run."""
    error = f"{type(exc).__name__}: {exc}"[:2_000]
    return [
        {
            "task_id": job["task_id"],
            "dataset": job.get("dataset"),
            "model": program_spec["model"],
            "config": program_spec["config"],
            "thinking": program_spec["thinking"],
            "status": "worker_error",
            "tests_total": 0,
            "tests_passed": 0,
            "error": error,
        }
        for program_spec in job["programs"]
    ]


def runner(
    *,
    max_workers: int = 4,
    max_in_flight: int = 8,
    timeout: float = 2.0,
    limit: int | None = None,
    output_path: Path | None = None,
    overwrite: bool = False,
) -> Path:
    """Evaluate streamed jobs with a bounded rolling queue and write CSV rows."""
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")
    if max_in_flight < max_workers:
        raise ValueError("max_in_flight must be at least max_workers")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    if limit is not None and limit < 1:
        raise ValueError("limit must be at least 1")
    if not JUDGE_PYTHON.is_file():
        raise FileNotFoundError(f"Judge Python not found: {JUDGE_PYTHON}")

    output_path = output_path or RESULTS_DIR / "correctness_results.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_mode = "w" if overwrite else "x"

    jobs: Iterator[dict[str, Any]] = iter(main_process())
    if limit is not None:
        jobs = iter(islice(jobs, limit))

    completed_jobs = 0
    with output_path.open(
        output_mode,
        encoding="utf-8",
        newline="",
    ) as output_file:
        writer = csv.DictWriter(output_file, fieldnames=RESULT_FIELDS)
        writer.writeheader()

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            pending = {}

            for _ in range(max_in_flight):
                try:
                    job = next(jobs)
                except StopIteration:
                    break

                future = executor.submit(evaluate_job, job, timeout)
                pending[future] = job

            while pending:
                done, _ = wait(pending, return_when=FIRST_COMPLETED)

                for finished_future in done:
                    finished_job = pending.pop(finished_future)
                    try:
                        results = finished_future.result()
                    except Exception as exc:
                        results = worker_error_results(finished_job, exc)

                    writer.writerows(results)
                    output_file.flush()
                    completed_jobs += 1
                    print(
                        f"\rCompleted {completed_jobs} benchmark jobs",
                        end="",
                        flush=True,
                    )

                    try:
                        next_job = next(jobs)
                    except StopIteration:
                        continue

                    new_future = executor.submit(evaluate_job, next_job, timeout)
                    pending[new_future] = next_job

    print()
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate Qwen scaling-law generations against benchmark tests."
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-in-flight", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument(
        "--limit",
        type=int,
        help="Evaluate only this many benchmark tasks (useful for a smoke test).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=RESULTS_DIR / "correctness_results.csv",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing output CSV.",
    )
    return parser.parse_args()


def cli() -> None:
    args = parse_args()
    output_path = runner(
        max_workers=args.workers,
        max_in_flight=args.max_in_flight,
        timeout=args.timeout,
        limit=args.limit,
        output_path=args.output,
        overwrite=args.overwrite,
    )
    print(f"Wrote results to {output_path}")


if __name__ == "__main__":
    cli()
