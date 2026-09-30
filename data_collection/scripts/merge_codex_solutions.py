"""Merge cleaned Codex reference solutions and traces by task ID."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_COLLECTION_DIR = PROJECT_ROOT / "data_collection"
NORMALIZED_DIR = DATA_COLLECTION_DIR / "normalized"
CODEX_DIR = DATA_COLLECTION_DIR / "reference_solutions" / "codex"
TRACE_DIR = PROJECT_ROOT / "complexity_metrics" / "traces"


def read_jsonl_as_lookup(path: Path, key: str = "task_id") -> dict[str, dict]:
    lookup = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                lookup[row[key]] = row
    return lookup


def replace_rows_by_task_id(
    input_path: Path,
    replacement_path: Path,
    output_path: Path,
) -> None:
    replacements = read_jsonl_as_lookup(replacement_path)
    replaced = total = 0
    with input_path.open("r", encoding="utf-8") as source, output_path.open(
        "w", encoding="utf-8"
    ) as destination:
        for line in source:
            if not line.strip():
                continue
            row = json.loads(line)
            total += 1
            if row["task_id"] in replacements:
                row = replacements[row["task_id"]]
                replaced += 1
            destination.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{input_path}: replaced {replaced}/{total}")


def main() -> None:
    for dataset in ("apps", "lcb"):
        replace_rows_by_task_id(
            NORMALIZED_DIR / f"{dataset}_test.jsonl",
            CODEX_DIR / f"{dataset}_test_data.jsonl",
            NORMALIZED_DIR / f"{dataset}_test_replaced.jsonl",
        )
        replace_rows_by_task_id(
            TRACE_DIR / f"{dataset}_test.jsonl",
            CODEX_DIR / f"{dataset}_test_traces.jsonl",
            TRACE_DIR / f"{dataset}_test_replaced.jsonl",
        )


if __name__ == "__main__":
    main()
