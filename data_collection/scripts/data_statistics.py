import ast
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_COLLECTION_DIR = PROJECT_ROOT / "data_collection"
REFERENCE_DIR = DATA_COLLECTION_DIR / "reference_solutions"
OUTPUT_FILE = DATA_COLLECTION_DIR / "outputs" / "data_statistics.txt"


DATA_FILES = {
    "mbpp_test": DATA_COLLECTION_DIR / "normalized" / "mbpp_test.jsonl",
    "humaneval_test": DATA_COLLECTION_DIR / "normalized" / "humaneval_test.jsonl",
    "apps_test": DATA_COLLECTION_DIR / "normalized" / "apps_test.jsonl",
    "lcb_test": DATA_COLLECTION_DIR / "normalized" / "lcb_test.jsonl",
}

MISSING_FILES = {
    "apps": REFERENCE_DIR / "missing" / "missing_apps.jsonl",
    "lcb": REFERENCE_DIR / "missing" / "missing_lcb.jsonl",
}

CODEX_FILES = {
    "apps": REFERENCE_DIR / "codex" / "apps_test_data.jsonl",
    "lcb": REFERENCE_DIR / "codex" / "lcb_test_data.jsonl",
}

REPLACED_DATA_FILES = {
    "apps": DATA_COLLECTION_DIR / "normalized" / "apps_test_replaced.jsonl",
    "lcb": DATA_COLLECTION_DIR / "normalized" / "lcb_test_replaced.jsonl",
}

REPLACED_TRACE_FILES = {
    "apps": PROJECT_ROOT / "complexity_metrics" / "traces" / "apps_test_replaced.jsonl",
    "lcb": PROJECT_ROOT / "complexity_metrics" / "traces" / "lcb_test_replaced.jsonl",
}

FAIR_DATA_FILES = {
    "mbpp_test": PROJECT_ROOT / "fair_data" / "data_jsonl" / "mbpp_test.jsonl",
    "humaneval_test": PROJECT_ROOT / "fair_data" / "data_jsonl" / "humaneval_test.jsonl",
    "apps_test": PROJECT_ROOT / "fair_data" / "data_jsonl" / "apps_test.jsonl",
    "lcb_test": PROJECT_ROOT / "fair_data" / "data_jsonl" / "lcb_test.jsonl",
}

FAIR_TRACE_FILES = {
    "mbpp_test": PROJECT_ROOT / "complexity_metrics" / "fair_traces" / "mbpp_test.jsonl",
    "humaneval_test": PROJECT_ROOT / "complexity_metrics" / "fair_traces" / "humaneval_test.jsonl",
    "apps_test": PROJECT_ROOT / "complexity_metrics" / "fair_traces" / "apps_test.jsonl",
    "lcb_test": PROJECT_ROOT / "complexity_metrics" / "fair_traces" / "lcb_test.jsonl",
}


def read_jsonl(path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def get_qids(path):
    return [row["task_id"] for row in read_jsonl(path)]


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


def ordered_intersection(left_ids, right_ids):
    right = set(right_ids)
    return [task_id for task_id in left_ids if task_id in right]


def format_id_list(title, ids):
    lines = [f"{title} ({len(ids)}):"]
    if ids:
        lines.extend(f"- {task_id}" for task_id in ids)
    else:
        lines.append("- None")
    return lines


def build_statistics():
    source_ids = {name: get_qids(path) for name, path in DATA_FILES.items()}
    missing_ids = {name: get_qids(path) for name, path in MISSING_FILES.items()}
    codex_ids = {name: get_qids(path) for name, path in CODEX_FILES.items()}
    fair_data_ids = {name: get_qids(path) for name, path in FAIR_DATA_FILES.items()}
    fair_trace_ids = {name: get_qids(path) for name, path in FAIR_TRACE_FILES.items()}

    replaced_data_rows = {
        name: read_jsonl(path)
        for name, path in REPLACED_DATA_FILES.items()
    }
    replaced_trace_rows = {
        name: read_jsonl(path)
        for name, path in REPLACED_TRACE_FILES.items()
    }

    ref_ids = {
        name: [row["task_id"] for row in rows if has_reference_solution(row)]
        for name, rows in replaced_data_rows.items()
    }
    trace_metric_ids = {
        name: [row["task_id"] for row in rows if has_trace_metrics(row)]
        for name, rows in replaced_trace_rows.items()
    }
    fair_eligible_ids = {
        name: ordered_intersection(ref_ids[name], trace_metric_ids[name])
        for name in ref_ids
    }

    unsolved_ids = {
        name: [task_id for task_id in missing_ids[name] if task_id not in set(codex_ids[name])]
        for name in missing_ids
    }

    return {
        "source_ids": source_ids,
        "missing_ids": missing_ids,
        "codex_ids": codex_ids,
        "unsolved_ids": unsolved_ids,
        "ref_ids": ref_ids,
        "trace_metric_ids": trace_metric_ids,
        "fair_eligible_ids": fair_eligible_ids,
        "fair_data_ids": fair_data_ids,
        "fair_trace_ids": fair_trace_ids,
    }


def write_report(stats, output_file=OUTPUT_FILE):
    source_ids = stats["source_ids"]
    missing_ids = stats["missing_ids"]
    codex_ids = stats["codex_ids"]
    unsolved_ids = stats["unsolved_ids"]
    ref_ids = stats["ref_ids"]
    trace_metric_ids = stats["trace_metric_ids"]
    fair_eligible_ids = stats["fair_eligible_ids"]
    fair_data_ids = stats["fair_data_ids"]
    fair_trace_ids = stats["fair_trace_ids"]

    lines = [
        "Data Statistics",
        "===============",
        "",
        "Source data counts",
        "------------------",
        f"MBPP test: {len(source_ids['mbpp_test'])}",
        f"HumanEval test: {len(source_ids['humaneval_test'])}",
        f"APPS test: {len(source_ids['apps_test'])}",
        f"LCB test: {len(source_ids['lcb_test'])}",
        "",
        "Missing reference-solution rows before Codex replacement",
        "-------------------------------------------------------",
        f"APPS missing: {len(missing_ids['apps'])}",
        f"LCB missing: {len(missing_ids['lcb'])}",
        "",
        "Solved by Codex",
        "---------------",
        f"APPS Codex solved: {len(codex_ids['apps'])}",
        f"LCB Codex solved: {len(codex_ids['lcb'])}",
        "",
        "Codex-unsolved rows from the missing set",
        "---------------------------------------",
        f"APPS unsolved: {len(unsolved_ids['apps'])}",
        f"LCB unsolved: {len(unsolved_ids['lcb'])}",
        "",
        "Replaced data counts",
        "--------------------",
        f"APPS replaced data rows: {len(get_qids(REPLACED_DATA_FILES['apps']))}",
        f"LCB replaced data rows: {len(get_qids(REPLACED_DATA_FILES['lcb']))}",
        "",
        "Reference/trace availability after replacement",
        "----------------------------------------------",
        f"APPS rows with reference solutions: {len(ref_ids['apps'])}",
        f"APPS rows with trace metrics: {len(trace_metric_ids['apps'])}",
        f"APPS rows with both reference solutions and trace metrics: {len(fair_eligible_ids['apps'])}",
        "",
        f"LCB rows with reference solutions: {len(ref_ids['lcb'])}",
        f"LCB rows with trace metrics: {len(trace_metric_ids['lcb'])}",
        f"LCB rows with both reference solutions and trace metrics: {len(fair_eligible_ids['lcb'])}",
        "",
        "Final fair_data counts",
        "----------------------",
        f"fair_data/data_jsonl/mbpp_test.jsonl: {len(fair_data_ids['mbpp_test'])}",
        f"fair_data/data_jsonl/humaneval_test.jsonl: {len(fair_data_ids['humaneval_test'])}",
        f"fair_data/data_jsonl/apps_test.jsonl: {len(fair_data_ids['apps_test'])}",
        f"fair_data/data_jsonl/lcb_test.jsonl: {len(fair_data_ids['lcb_test'])}",
        "",
        f"complexity_metrics/fair_traces/mbpp_test.jsonl: {len(fair_trace_ids['mbpp_test'])}",
        f"complexity_metrics/fair_traces/humaneval_test.jsonl: {len(fair_trace_ids['humaneval_test'])}",
        f"complexity_metrics/fair_traces/apps_test.jsonl: {len(fair_trace_ids['apps_test'])}",
        f"complexity_metrics/fair_traces/lcb_test.jsonl: {len(fair_trace_ids['lcb_test'])}",
        "",
        f"Total fair_data rows: {sum(len(ids) for ids in fair_data_ids.values())}",
        "",
        "Filtering rule",
        "--------------",
        "A row is kept in fair_data only if:",
        "1. the data row contains a non-empty reference_solutions field, and",
        "2. the matching trace row contains trace metrics, checked by AST_Length.",
        "",
        "Important ID lists",
        "------------------",
    ]

    lines.extend(format_id_list("APPS missing IDs", missing_ids["apps"]))
    lines.append("")
    lines.extend(format_id_list("APPS Codex-solved IDs", codex_ids["apps"]))
    lines.append("")
    lines.extend(format_id_list("APPS unsolved IDs", unsolved_ids["apps"]))
    lines.append("")
    lines.extend(format_id_list("LCB missing IDs", missing_ids["lcb"]))
    lines.append("")
    lines.extend(format_id_list("LCB Codex-solved IDs", codex_ids["lcb"]))
    lines.append("")
    lines.extend(format_id_list("LCB unsolved IDs", unsolved_ids["lcb"]))
    lines.append("")
    lines.extend(format_id_list("Fair APPS IDs", fair_data_ids["apps_test"]))
    lines.append("")
    lines.extend(format_id_list("Fair LCB IDs", fair_data_ids["lcb_test"]))

    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    stats = build_statistics()
    write_report(stats)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
