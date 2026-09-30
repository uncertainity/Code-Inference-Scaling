import argparse
import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = BASE_DIR / "fair_data" / "data_jsonl" / "apps_test.jsonl"
DEFAULT_OUT = BASE_DIR / "fair_data" / "test_results" / "apps_results.jsonl"


def read_jsonl(path):
    rows = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_maybe_encoded(value):
    if not isinstance(value, str):
        return value

    text = value.strip()
    if not text:
        return value

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    try:
        return ast.literal_eval(text)
    except (SyntaxError, ValueError):
        return value


def first_reference_solution(row):
    refs = parse_maybe_encoded(row.get("reference_solutions"))
    if isinstance(refs, list):
        for code in refs:
            if isinstance(code, str) and code.strip():
                return code
    if isinstance(refs, str) and refs.strip():
        return refs
    return None


def candidate_code(row):
    for key in ("generated_code", "genrated_code", "code", "completion"):
        code = row.get(key)
        if isinstance(code, str) and code.strip():
            return code
    return first_reference_solution(row)


def stdio_cases(row):
    tests = parse_maybe_encoded(row.get("tests"))

    if isinstance(tests, dict) and "inputs" in tests and "outputs" in tests:
        return [
            {"input": test_input, "output": test_output}
            for test_input, test_output in zip(tests["inputs"], tests["outputs"])
        ]

    if isinstance(tests, list):
        cases = []
        for test in tests:
            if not isinstance(test, dict):
                continue
            if "input" in test and "output" in test:
                cases.append({"input": test["input"], "output": test["output"]})
        return cases

    return []


def same_output(actual, expected):
    return actual.strip() == expected.strip()


def run_code_on_input(code, test_input, timeout):
    with tempfile.TemporaryDirectory(prefix="fair_test_") as tmpdir:
        script_path = Path(tmpdir) / "solution.py"
        script_path.write_text(code, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=tmpdir,
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "ok": False,
                "status": "timeout",
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "",
            }

    if proc.returncode != 0:
        return {
            "ok": False,
            "status": "runtime_error",
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    return {
        "ok": True,
        "status": "ok",
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def run_stdio_row(row, code, timeout, max_tests_per_task):
    cases = stdio_cases(row)
    available_tests = len(cases)
    if max_tests_per_task is not None:
        cases = cases[:max_tests_per_task]

    if not cases:
        return {
            "task_id": row.get("task_id"),
            "dataset": row.get("dataset"),
            "passed": False,
            "passed_tests": 0,
            "total_tests": 0,
            "available_tests": available_tests,
            "status": "no_tests",
            "first_failure": None,
        }

    for idx, case in enumerate(cases):
        run = run_code_on_input(code, case["input"], timeout)
        if not run["ok"]:
            return {
                "task_id": row.get("task_id"),
                "dataset": row.get("dataset"),
                "passed": False,
                "passed_tests": idx,
                "total_tests": len(cases),
                "available_tests": available_tests,
                "status": run["status"],
                "first_failure": {
                    "test_index": idx,
                    "input": case["input"],
                    "expected": case["output"],
                    "stdout": run["stdout"],
                    "stderr": run["stderr"],
                },
            }

        if not same_output(run["stdout"], case["output"]):
            return {
                "task_id": row.get("task_id"),
                "dataset": row.get("dataset"),
                "passed": False,
                "passed_tests": idx,
                "total_tests": len(cases),
                "available_tests": available_tests,
                "status": "wrong_answer",
                "first_failure": {
                    "test_index": idx,
                    "input": case["input"],
                    "expected": case["output"],
                    "stdout": run["stdout"],
                    "stderr": run["stderr"],
                },
            }

    return {
        "task_id": row.get("task_id"),
        "dataset": row.get("dataset"),
        "passed": True,
        "passed_tests": len(cases),
        "total_tests": len(cases),
        "available_tests": available_tests,
        "status": "accepted",
        "first_failure": None,
    }


def load_generation_map(path):
    if path is None:
        return None
    return {row["task_id"]: row for row in read_jsonl(path)}


def run_tests(data_path, generations_path, output_path, limit, timeout, max_tests_per_task):
    data_rows = read_jsonl(data_path)
    generation_by_id = load_generation_map(generations_path)
    results = []

    for row in data_rows:
        if generation_by_id is not None:
            gen_row = generation_by_id.get(row["task_id"])
            if gen_row is None:
                continue
            code = candidate_code(gen_row)
        else:
            code = candidate_code(row)

        if not code:
            results.append(
                {
                    "task_id": row.get("task_id"),
                    "dataset": row.get("dataset"),
                    "passed": False,
                    "passed_tests": 0,
                    "total_tests": len(stdio_cases(row)),
                    "available_tests": len(stdio_cases(row)),
                    "status": "missing_code",
                    "first_failure": None,
                }
            )
        elif row.get("test_type") == "stdin_stdout":
            results.append(run_stdio_row(row, code, timeout, max_tests_per_task))
        else:
            results.append(
                {
                    "task_id": row.get("task_id"),
                    "dataset": row.get("dataset"),
                    "passed": False,
                    "passed_tests": 0,
                    "total_tests": 0,
                    "available_tests": 0,
                    "status": f"unsupported_test_type:{row.get('test_type')}",
                    "first_failure": None,
                }
            )

        if limit is not None and len(results) >= limit:
            break

    write_jsonl(output_path, results)
    passed = sum(1 for row in results if row["passed"])
    print(f"wrote {len(results)} results to {output_path}")
    print(f"passed tasks: {passed}/{len(results)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--generations", default=None)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--max-tests-per-task", type=int, default=None)
    args = parser.parse_args()

    run_tests(
        args.data,
        args.generations,
        args.out,
        args.limit,
        args.timeout,
        args.max_tests_per_task,
    )


if __name__ == "__main__":
    main()
