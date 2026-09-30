from __future__ import annotations

import argparse
import json
import re
import zlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def is_severe_repetition(text: str) -> bool:
    tokens = [token.lower() for token in TOKEN_RE.findall(text)]
    if len(tokens) >= 12:
        ngrams = Counter(tuple(tokens[i : i + 12]) for i in range(len(tokens) - 11))
        if ngrams and max(ngrams.values()) >= 20:
            return True

    lines = [" ".join(line.lower().split()) for line in text.splitlines()]
    nontrivial_lines = [line for line in lines if len(line) >= 20]
    if nontrivial_lines and max(Counter(nontrivial_lines).values()) >= 15:
        return True

    encoded = text.encode("utf-8")
    return len(encoded) > 3000 and len(zlib.compress(encoded)) / len(encoded) < 0.12


def has_final_answer(text: str, thinking: bool) -> bool:
    if not thinking:
        return bool(text.strip())
    marker = "</think>"
    return marker in text and bool(text.rsplit(marker, 1)[1].strip())


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def summarize_config(config_dir: Path) -> dict[str, Any]:
    config = json.loads((config_dir / "config.json").read_text(encoding="utf-8"))
    sampling = config.get("sampling_params", config)
    thinking = bool(sampling.get("chat_template_kwargs", {}).get("enable_thinking", False))
    by_dataset: dict[str, dict[str, Any]] = {}

    for result_path in sorted(config_dir.glob("*_generations.jsonl")):
        rows = load_rows(result_path)
        dataset = result_path.name[: -len("_generations.jsonl")]
        repeated_ids = []
        completion_tokens = []
        normal = final = nonempty = 0

        for row in rows:
            prediction = row.get("prediction") or ""
            finish_reason = row.get("finish_reason")
            usage = row.get("usage") or {}
            tokens = usage.get("completion_tokens")
            if isinstance(tokens, (int, float)):
                completion_tokens.append(float(tokens))
            normal += finish_reason == "stop"
            nonempty += bool(prediction.strip())
            final += has_final_answer(prediction, thinking)
            if is_severe_repetition(prediction):
                repeated_ids.append(str(row.get("task_id", "<missing-task-id>")))

        by_dataset[dataset] = {
            "total": len(rows),
            "normal": normal,
            "nonempty": nonempty,
            "final": final,
            "repeated_ids": repeated_ids,
            "avg_tokens": sum(completion_tokens) / len(completion_tokens) if completion_tokens else 0.0,
        }

    totals = {
        "total": sum(item["total"] for item in by_dataset.values()),
        "normal": sum(item["normal"] for item in by_dataset.values()),
        "nonempty": sum(item["nonempty"] for item in by_dataset.values()),
        "final": sum(item["final"] for item in by_dataset.values()),
        "repeated_ids": [task_id for item in by_dataset.values() for task_id in item["repeated_ids"]],
    }
    token_count = sum(item["total"] for item in by_dataset.values())
    totals["avg_tokens"] = (
        sum(item["avg_tokens"] * item["total"] for item in by_dataset.values()) / token_count
        if token_count
        else 0.0
    )
    return {"name": config_dir.name, "thinking": thinking, "datasets": by_dataset, **totals}


def fraction(value: int, total: int) -> str:
    percent = 100.0 * value / total if total else 0.0
    return f"{value}/{total} ({percent:.1f}%)"


def render_model(model_dir: Path, summaries: list[dict[str, Any]]) -> str:
    ranked = sorted(
        summaries,
        key=lambda item: (-item["normal"], len(item["repeated_ids"]), item["avg_tokens"]),
    )
    lines = [
        f"# {model_dir.name} completion and repetition report",
        "",
        f"Generated from `{model_dir}`. Completion health is not code correctness; generated programs have not been evaluated by the test harness here.",
        "",
        "## Overall ranking",
        "",
        "| Configuration | Thinking | Normal stops | Final answers | Severe repetition | Average completion tokens |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in ranked:
        lines.append(
            f"| `{item['name']}` | {'Yes' if item['thinking'] else 'No'} | "
            f"{fraction(item['normal'], item['total'])} | {fraction(item['final'], item['total'])} | "
            f"{len(item['repeated_ids'])}/{item['total']} | {item['avg_tokens']:,.1f} |"
        )

    lines += ["", "## Dataset details", ""]
    for item in ranked:
        lines += [
            f"### `{item['name']}`",
            "",
            "| Dataset | Normal stops | Final/non-empty answers | Severe repetition | Average completion tokens |",
            "|---|---:|---:|---:|---:|",
        ]
        for dataset, result in sorted(item["datasets"].items()):
            answer_count = result["final"] if item["thinking"] else result["nonempty"]
            lines.append(
                f"| {dataset} | {fraction(result['normal'], result['total'])} | "
                f"{fraction(answer_count, result['total'])} | {len(result['repeated_ids'])}/{result['total']} | "
                f"{result['avg_tokens']:,.1f} |"
            )
        repeated = item["repeated_ids"]
        lines += [
            "",
            "Severe repetition flags: " + (", ".join(f"`{task_id}`" for task_id in repeated) if repeated else "none."),
            "",
        ]

    lines += [
        "## Definitions",
        "",
        "- A normal stop has `finish_reason == \"stop\"`; `length` means the request reached its token limit.",
        "- A thinking final answer requires a closed `</think>` block followed by non-empty content.",
        "- Severe repetition means a normalized 12-token sequence appears at least 20 times, a non-trivial line appears at least 15 times, or text over 3,000 bytes compresses below 12% of its original size.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Report vLLM completion and repetition statistics.")
    parser.add_argument("run_dir", type=Path, help="Run directory containing models/<model>/<config>.")
    args = parser.parse_args()

    models_dir = args.run_dir / "models"
    aggregate: list[tuple[str, list[dict[str, Any]]]] = []
    for model_dir in sorted(path for path in models_dir.iterdir() if path.is_dir()):
        summaries = [summarize_config(path) for path in sorted(model_dir.iterdir()) if path.is_dir()]
        report = render_model(model_dir, summaries)
        (model_dir / "completion_repetition_report.md").write_text(report, encoding="utf-8")
        aggregate.append((model_dir.name, summaries))

    lines = [
        "# Multi-model completion and repetition summary",
        "",
        f"Generated from `{args.run_dir}`. These are generation-health statistics, not test-pass rates.",
        "",
        "| Model | Best normal-stop config | Normal stops | Repetition | Best thinking config | Thinking final answers | Repetition |",
        "|---|---|---:|---:|---|---:|---:|",
    ]
    for model, summaries in aggregate:
        overall = min(summaries, key=lambda x: (-x["normal"], len(x["repeated_ids"]), x["avg_tokens"]))
        thinking_items = [item for item in summaries if item["thinking"]]
        thinking = min(thinking_items, key=lambda x: (-x["final"], len(x["repeated_ids"]), x["avg_tokens"]))
        lines.append(
            f"| {model} | `{overall['name']}` | {fraction(overall['normal'], overall['total'])} | "
            f"{len(overall['repeated_ids'])}/{overall['total']} | `{thinking['name']}` | "
            f"{fraction(thinking['final'], thinking['total'])} | {len(thinking['repeated_ids'])}/{thinking['total']} |"
        )
    lines += ["", "Detailed reports are stored inside each model directory.", ""]
    (args.run_dir / "completion_repetition_report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
