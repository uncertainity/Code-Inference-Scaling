from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Any

try:
    from .normalizer import TestCase, parse_test_cases
except ImportError:  # Support `python test_harness/evaluator.py` imports.
    from normalizer import TestCase, parse_test_cases


HARNESS_DIR = Path(__file__).resolve().parent
JUDGE_PYTHON = HARNESS_DIR / ".venv" / "bin" / "python"
MAX_DIAGNOSTIC_CHARS = 2_000


def evaluate_job(job: dict[str, Any], timeout: float = 2.0) -> list[dict[str, Any]]:
    """Evaluate all model/config programs for one benchmark task."""
    programs = job["programs"]

    try:
        tests = parse_test_cases(job["tests"])
    except ValueError as exc:
        return [
            {
                **result_metadata(job, program_spec),
                "status": "unsupported_test_format",
                "tests_total": 0,
                "tests_passed": 0,
                "error": str(exc),
            }
            for program_spec in programs
        ]

    results = []
    for program_spec in programs:
        outcome = evaluate_program(program_spec, tests, timeout=timeout)
        results.append(
            {
                **result_metadata(job, program_spec),
                **outcome,
            }
        )

    return results


def result_metadata(
    job: dict[str, Any],
    program_spec: dict[str, Any],
) -> dict[str, Any]:
    """Return fields identifying one task/model/config evaluation."""
    return {
        "task_id": job["task_id"],
        "dataset": job.get("dataset"),
        "model": program_spec["model"],
        "config": program_spec["config"],
        "thinking": program_spec["thinking"],
    }


def evaluate_program(
    program_spec: dict[str, Any],
    tests: list[TestCase],
    timeout: float = 2.0,
) -> dict[str, Any]:
    """Run one normalized program against a task's tests, stopping at first failure."""
    normalized = program_spec["normalized"]
    tests_total = len(tests)

    if normalized.status != "ok" or normalized.code is None:
        status = normalized.status if normalized.status != "ok" else "missing_code"
        result = {
            "status": status,
            "tests_total": tests_total,
            "tests_passed": 0,
        }
        if normalized.syntax_error:
            result["error"] = normalized.syntax_error
        return result

    with tempfile.TemporaryDirectory(prefix="judge_") as temp_dir:
        program_path = Path(temp_dir) / "solution.py"
        program_path.write_text(normalized.code, encoding="utf-8")

        for test_index, test_case in enumerate(tests):
            try:
                completed = subprocess.run(
                    [str(JUDGE_PYTHON), str(program_path)],
                    input=test_case.stdin,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    capture_output=True,
                    timeout=timeout,
                    cwd=temp_dir,
                )
            except subprocess.TimeoutExpired:
                return failure_result(
                    status="timeout",
                    test_index=test_index,
                    tests_total=tests_total,
                    test_case=test_case,
                )

            if completed.returncode != 0:
                return failure_result(
                    status="runtime_error",
                    test_index=test_index,
                    tests_total=tests_total,
                    test_case=test_case,
                    actual=completed.stdout,
                    stderr=completed.stderr,
                    returncode=completed.returncode,
                )

            if completed.stdout.strip() != test_case.expected_stdout.strip():
                return failure_result(
                    status="wrong_answer",
                    test_index=test_index,
                    tests_total=tests_total,
                    test_case=test_case,
                    actual=completed.stdout,
                    stderr=completed.stderr,
                )

    return {
        "status": "accepted",
        "tests_total": tests_total,
        "tests_passed": tests_total,
    }


def failure_result(
    *,
    status: str,
    test_index: int,
    tests_total: int,
    test_case: TestCase,
    actual: str = "",
    stderr: str = "",
    returncode: int | None = None,
) -> dict[str, Any]:
    """Build a compact first-failure record for later analysis."""
    result = {
        "status": status,
        "tests_total": tests_total,
        "tests_passed": test_index,
        "failed_test_index": test_index,
        "input": truncate(test_case.stdin),
        "expected": truncate(test_case.expected_stdout),
        "actual": truncate(actual),
        "stderr": truncate(stderr),
    }
    if returncode is not None:
        result["returncode"] = returncode
    return result


def truncate(text: str) -> str:
    """Keep failure diagnostics from making the result JSONL excessively large."""
    return text[:MAX_DIAGNOSTIC_CHARS]
