import argparse
import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path

# from sortedcontainers import SortedList
# import scipy
# import atcoder
# pip install numpy scipy networkx numba


# python3 arka/Compression_Law/run_fair_test_1.py \
#   --generations arka/Compression_Law/fair_data/test_results/apps_subset.jsonl \
#   --out arka/Compression_Law/fair_data/test_results/custom_results.jsonl

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "fair_data" / "data_jsonl"
RESULTS_DIR = BASE_DIR / "fair_data" / "test_results"

DATASETS = {
    "apps": DATA_DIR / "apps_test.jsonl",
    "mbpp": DATA_DIR / "mbpp_test.jsonl",
    "humaneval": DATA_DIR / "humaneval_test.jsonl",
    "lcb": DATA_DIR / "lcb_test.jsonl",
}


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

    for key in ("reference_code", "referrence_code"):
        code = row.get(key)
        if isinstance(code, str) and code.strip():
            return code
    return None


def strip_code_fence(code):
    if not isinstance(code, str):
        return code

    lines = code.strip().splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip() + "\n"
    return code


def candidate_code(row):
    for key in ("generated_code", "genrated_code", "code", "completion"):
        code = row.get(key)
        if isinstance(code, str) and code.strip():
            return strip_code_fence(code)
    return first_reference_solution(row)


def subset_row_from_data_row(row):
    return {
        "task_id": row.get("task_id"),
        "dataset": row.get("dataset"),
        "split": row.get("split"),
        "prompt_type": row.get("prompt_type"),
        "test_type": row.get("test_type"),
        "entry_point": row.get("entry_point"),
        "prompt": row.get("prompt"),
        "tests": row.get("tests"),
        "generated_code": first_reference_solution(row),
    }


def create_subset(dataset_name, data_path, output_path, limit):
    rows = read_jsonl(data_path)
    if limit is not None:
        rows = rows[:limit]

    subset_rows = [subset_row_from_data_row(row) for row in rows]
    write_jsonl(output_path, subset_rows)
    print(f"wrote {len(subset_rows)} simulated generations to {output_path}")


def selected_dataset_names(dataset_arg):
    if dataset_arg == "all":
        return list(DATASETS)
    return [dataset_arg]


def subset_path(dataset_name):
    return RESULTS_DIR / f"{dataset_name}_subset.jsonl"


def result_path(dataset_name):
    return RESULTS_DIR / f"{dataset_name}_results.jsonl"


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


def assertion_test_code(row, max_tests_per_task):
    tests = parse_maybe_encoded(row.get("tests"))

    if isinstance(tests, str):
        return tests, tests.count("assert ")

    if isinstance(tests, dict):
        setup = tests.get("test_setup_code") or ""
        test_lines = []
        test_lines.extend(tests.get("test_list") or [])
        test_lines.extend(tests.get("challenge_test_list") or [])
        available_tests = len(test_lines)
        if max_tests_per_task is not None:
            test_lines = test_lines[:max_tests_per_task]
        return "\n".join([setup, *test_lines, ""]), available_tests

    if isinstance(tests, list):
        test_lines = [test for test in tests if isinstance(test, str)]
        available_tests = len(test_lines)
        if max_tests_per_task is not None:
            test_lines = test_lines[:max_tests_per_task]
        return "\n".join(test_lines) + "\n", available_tests

    return "", 0


def same_output(actual, expected):
    return actual.strip() == expected.strip()


def run_python_script(code, timeout, stdin_text=""):
    with tempfile.TemporaryDirectory(prefix="fair_test_") as tmpdir:
        script_path = Path(tmpdir) / "solution.py"
        script_path.write_text(code, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                input=stdin_text,
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
        status = "assertion_error" if "AssertionError" in proc.stderr else "runtime_error"
        return {
            "ok": False,
            "status": status,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    return {
        "ok": True,
        "status": "ok",
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def run_code_on_input(code, test_input, timeout):
    return run_python_script(code, timeout, stdin_text=test_input)


def run_stdio_row(row, code, timeout, max_tests_per_task):
    cases = stdio_cases(row)
    available_tests = len(cases)
    if max_tests_per_task is not None:
        cases = cases[:max_tests_per_task]

    if not cases:
        return failure_result(row, "no_tests", 0, 0, available_tests)

    for idx, case in enumerate(cases):
        run = run_code_on_input(code, case["input"], timeout)
        if not run["ok"]:
            return failure_result(
                row,
                run["status"],
                idx,
                len(cases),
                available_tests,
                {
                    "test_index": idx,
                    "input": case["input"],
                    "expected": case["output"],
                    "stdout": run["stdout"],
                    "stderr": run["stderr"],
                },
            )

        if not same_output(run["stdout"], case["output"]):
            return failure_result(
                row,
                "wrong_answer",
                idx,
                len(cases),
                available_tests,
                {
                    "test_index": idx,
                    "input": case["input"],
                    "expected": case["output"],
                    "stdout": run["stdout"],
                    "stderr": run["stderr"],
                },
            )

    return accepted_result(row, len(cases), available_tests)


def defines_entry_point(code, entry_point):
    if not entry_point:
        return False
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    return any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == entry_point
        for node in tree.body
    )


def candidate_with_prompt_if_needed(row, code):
    entry_point = row.get("entry_point")
    prompt = row.get("prompt")
    if entry_point and prompt and not defines_entry_point(code, entry_point):
        return prompt.rstrip() + "\n" + code.rstrip() + "\n"
    return code.rstrip() + "\n"


def run_assertion_row(row, code, timeout, max_tests_per_task):
    test_code, available_tests = assertion_test_code(row, max_tests_per_task)
    total_tests = available_tests
    if max_tests_per_task is not None and not isinstance(parse_maybe_encoded(row.get("tests")), str):
        total_tests = min(available_tests, max_tests_per_task)

    if not test_code.strip():
        return failure_result(row, "no_tests", 0, 0, available_tests)

    script = candidate_with_prompt_if_needed(row, code)
    script += "\n" + test_code.rstrip() + "\n"

    entry_point = row.get("entry_point")
    if entry_point and "def check(" in test_code:
        script += f"\ncheck({entry_point})\n"

    run = run_python_script(script, timeout)
    if not run["ok"]:
        return failure_result(
            row,
            run["status"],
            0,
            total_tests,
            available_tests,
            {
                "stdout": run["stdout"],
                "stderr": run["stderr"],
            },
        )

    return accepted_result(row, total_tests, available_tests)


def accepted_result(row, total_tests, available_tests):
    return {
        "task_id": row.get("task_id"),
        "dataset": row.get("dataset"),
        "passed": True,
        "passed_tests": total_tests,
        "total_tests": total_tests,
        "available_tests": available_tests,
        "status": "accepted",
        "first_failure": None,
    }


def failure_result(row, status, passed_tests, total_tests, available_tests, first_failure=None):
    return {
        "task_id": row.get("task_id"),
        "dataset": row.get("dataset"),
        "passed": False,
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "available_tests": available_tests,
        "status": status,
        "first_failure": first_failure,
    }


def run_generated_rows(generations_path, output_path, limit, timeout, max_tests_per_task):
    rows = read_jsonl(generations_path)
    results = []

    for row in rows:
        code = candidate_code(row)
        test_type = row.get("test_type")
        prompt_type = row.get("prompt_type")

        if not code:
            available_tests = len(stdio_cases(row)) if test_type == "stdin_stdout" else 0
            results.append(failure_result(row, "missing_code", 0, 0, available_tests))
        elif test_type == "stdin_stdout":
            results.append(run_stdio_row(row, code, timeout, max_tests_per_task))
        elif test_type == "assertion" or prompt_type == "function":
            results.append(run_assertion_row(row, code, timeout, max_tests_per_task))
        else:
            results.append(failure_result(row, f"unsupported_test_type:{test_type}", 0, 0, 0))

        if limit is not None and len(results) >= limit:
            break

    write_jsonl(output_path, results)
    passed = sum(1 for row in results if row["passed"])
    print(f"wrote {len(results)} results to {output_path}")
    print(f"passed tasks: {passed}/{len(results)}")


def create_selected_subsets(dataset_arg, limit):
    for dataset_name in selected_dataset_names(dataset_arg):
        create_subset(dataset_name, DATASETS[dataset_name], subset_path(dataset_name), limit)


def evaluate_selected_subsets(dataset_arg, limit, timeout, max_tests_per_task):
    for dataset_name in selected_dataset_names(dataset_arg):
        run_generated_rows(
            subset_path(dataset_name),
            result_path(dataset_name),
            limit,
            timeout,
            max_tests_per_task,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("make-subsets", "evaluate", "all"), default="all")
    parser.add_argument("--dataset", choices=("all", *DATASETS.keys()), default="all")
    parser.add_argument("--generations", default=None)
    parser.add_argument("--out", default=None)
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--eval-limit", type=int, default=None)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--max-tests-per-task", type=int, default=None)
    args = parser.parse_args()

    if args.generations:
        output_path = args.out or RESULTS_DIR / "custom_results.jsonl"
        run_generated_rows(
            args.generations,
            output_path,
            args.eval_limit,
            args.timeout,
            args.max_tests_per_task,
        )
        return

    if args.mode in ("make-subsets", "all"):
        create_selected_subsets(args.dataset, args.limit)

    if args.mode in ("evaluate", "all"):
        evaluate_selected_subsets(
            args.dataset,
            args.eval_limit,
            args.timeout,
            args.max_tests_per_task,
        )


if __name__ == "__main__":
    main()
