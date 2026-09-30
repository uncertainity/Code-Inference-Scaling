import ast
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = Path(__file__).resolve().parent
TRACE_OUTPUT_DIR = PROJECT_ROOT / "complexity_metrics" / "fair_traces"

DATASETS = [
    {
        "name": "mbpp_test",
        "data": PROJECT_ROOT / "data_collection" / "normalized" / "mbpp_test.jsonl",
        "traces": PROJECT_ROOT / "complexity_metrics" / "traces" / "mbpp_test.jsonl",
    },
    {
        "name": "humaneval_test",
        "data": PROJECT_ROOT / "data_collection" / "normalized" / "humaneval_test.jsonl",
        "traces": PROJECT_ROOT / "complexity_metrics" / "traces" / "humaneval_test.jsonl",
    },
    {
        "name": "apps_test",
        "data": PROJECT_ROOT / "data_collection" / "normalized" / "apps_test_replaced.jsonl",
        "traces": PROJECT_ROOT / "complexity_metrics" / "traces" / "apps_test_replaced.jsonl",
    },
    {
        "name": "lcb_test",
        "data": PROJECT_ROOT / "data_collection" / "normalized" / "lcb_test_replaced.jsonl",
        "traces": PROJECT_ROOT / "complexity_metrics" / "traces" / "lcb_test_replaced.jsonl",
    },
]


def read_jsonl(path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def has_reference_solution(row):
    refs = row.get("reference_solutions")
    if refs is None:
        return False
    if isinstance(refs, (list, tuple)):
        return any(isinstance(code, str) and code.strip() for code in refs)
    if isinstance(refs, str):
        text = refs.strip()
        if not text:
            return False
        try:
            parsed = ast.literal_eval(text)
        except (SyntaxError, ValueError):
            return True
        if isinstance(parsed, (list, tuple)):
            return any(isinstance(code, str) and code.strip() for code in parsed)
        return isinstance(parsed, str) and bool(parsed.strip())
    return False


def has_trace_metrics(row):
    return "AST_Length" in row


def filter_dataset(spec):
    data_rows = read_jsonl(spec["data"])
    trace_rows = read_jsonl(spec["traces"])

    data_by_id = {
        row["task_id"]: row
        for row in data_rows
        if has_reference_solution(row)
    }
    trace_by_id = {
        row["task_id"]: row
        for row in trace_rows
        if has_trace_metrics(row)
    }

    keep_ids = set(data_by_id) & set(trace_by_id)
    filtered_data = [row for row in data_rows if row["task_id"] in keep_ids]
    filtered_traces = [row for row in trace_rows if row["task_id"] in keep_ids]

    data_out = OUTPUT_DIR / "data_jsonl" / f"{spec['name']}.jsonl"
    traces_out = TRACE_OUTPUT_DIR / f"{spec['name']}.jsonl"
    write_jsonl(data_out, filtered_data)
    write_jsonl(traces_out, filtered_traces)

    print(
        f"{spec['name']}: kept {len(keep_ids)} "
        f"from data={len(data_rows)} traces={len(trace_rows)}"
    )


def main():
    for spec in DATASETS:
        filter_dataset(spec)


if __name__ == "__main__":
    main()
