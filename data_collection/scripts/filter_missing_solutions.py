"""Collect APPS/LCB rows whose reference solutions lack complexity traces."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
NORMALIZED_DIR = PROJECT_ROOT / "data_collection" / "normalized"
TRACE_DIR = PROJECT_ROOT / "complexity_metrics" / "traces"
OUTPUT_DIR = PROJECT_ROOT / "data_collection" / "reference_solutions" / "missing"


def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def missing_trace_ids(path: Path) -> set[str]:
    return {
        row["task_id"]
        for row in read_jsonl(path)
        if "AST_Length" not in row
    }


def write_missing(dataset: str) -> int:
    missing_ids = missing_trace_ids(TRACE_DIR / f"{dataset}_test.jsonl")
    rows = [
        row
        for row in read_jsonl(NORMALIZED_DIR / f"{dataset}_test.jsonl")
        if row["task_id"] in missing_ids
    ]
    output_path = OUTPUT_DIR / f"missing_{dataset}.jsonl"
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for dataset in ("apps", "lcb"):
        print(f"{dataset}: wrote {write_missing(dataset)} missing rows")


if __name__ == "__main__":
    main()
