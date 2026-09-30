import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INPUTS = {
    "apps": BASE_DIR / "missing_solutions" / "missing_apps.jsonl",
    "lcb": BASE_DIR / "missing_solutions" / "missing_lcb.jsonl",
}
OUTPUTS = {
    "apps": BASE_DIR / "codex_solutions" / "apps_test",
    "lcb": BASE_DIR / "codex_solutions" / "lcb_test",
}


def parse_tests(raw_tests):
    if raw_tests in (None, ""):
        return []
    tests = json.loads(raw_tests) if isinstance(raw_tests, str) else raw_tests
    pairs = []

    if isinstance(tests, dict):
        inputs = tests.get("inputs", [])
        outputs = tests.get("outputs", [])
        pairs.extend(zip(inputs, outputs))
    elif isinstance(tests, list):
        for test in tests:
            if not isinstance(test, dict):
                continue
            if "input" in test and "output" in test:
                pairs.append((test["input"], test["output"]))
            elif "inputs" in test and "outputs" in test:
                pairs.extend(zip(test["inputs"], test["outputs"]))

    return pairs


def solution_source(task_id, pairs):
    raise RuntimeError(
        f"{task_id}: refusing to generate a public-test lookup table. "
        "Write a general algorithmic solution for this task instead."
    )


def task_filename(task_id):
    return f"{task_id.split('/', 1)[-1]}.py"


def generate(dataset):
    output_dir = OUTPUTS[dataset]
    output_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    skipped = 0

    with INPUTS[dataset].open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            pairs = parse_tests(row.get("tests"))
            if not pairs:
                skipped += 1
                continue

            path = output_dir / task_filename(row["task_id"])
            path.write_text(solution_source(row["task_id"], pairs), encoding="utf-8")
            written += 1

    return written, skipped


def main():
    for dataset in ("apps", "lcb"):
        written, skipped = generate(dataset)
        print(f"{dataset}: wrote {written}, skipped {skipped}")


if __name__ == "__main__":
    main()
