import pandas as pd
import os 
import json
from pathlib import Path
from io import StringIO
import tokenize
import ast
import io
import keyword
import textwrap
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import date, datetime

from datasets import DatasetDict, load_from_disk


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _trace_tools():
    from complexity_metrics.ast_metrics import getTraces, RadonMetrics

    return getTraces, RadonMetrics

class RemoveDocstrings(ast.NodeTransformer):
    def _remove_docstring(self, node):
        self.generic_visit(node)

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        return node

    def visit_Module(self, node):
        return self._remove_docstring(node)

    def visit_ClassDef(self, node):
        return self._remove_docstring(node)

    def visit_FunctionDef(self, node):
        return self._remove_docstring(node)

    def visit_AsyncFunctionDef(self, node):
        return self._remove_docstring(node)


def remove_comments(source):
    result = []

    tokens = tokenize.generate_tokens(StringIO(source).readline)

    for token in tokens:
        token_type = token.type
        token_string = token.string

        if token_type == tokenize.COMMENT:
            continue

        result.append(token)

    return tokenize.untokenize(result)


def _clean_source(code):
    code = code.encode("utf-8", errors="ignore").decode("utf-8")
    return _normalize_numeric_keyword_spacing(code)


def _normalize_numeric_keyword_spacing(code):
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    except (IndentationError, tokenize.TokenError):
        return code

    edits_by_line = {}
    for cur_token, next_token in zip(tokens, tokens[1:]):
        if cur_token.type != tokenize.NUMBER or next_token.type != tokenize.NAME:
            continue
        if next_token.string not in keyword.kwlist:
            continue
        if cur_token.end[0] != next_token.start[0]:
            continue
        if cur_token.end[1] != next_token.start[1]:
            continue
        edits_by_line.setdefault(cur_token.end[0], set()).add(cur_token.end[1])

    if not edits_by_line:
        return code

    lines = code.splitlines(keepends=True)
    for line_no, columns in edits_by_line.items():
        if line_no < 1 or line_no > len(lines):
            continue
        line = lines[line_no - 1]
        for column in sorted(columns, reverse=True):
            if 0 <= column <= len(line):
                line = line[:column] + " " + line[column:]
        lines[line_no - 1] = line
    return "".join(lines)


def normalize_lcb(row, split=None):
    metadata = {
        "platform": row.get("platform"),
        "question_title": row.get("question_title"),
        "question_id": row.get("question_id"),
        "contest_id": row.get("contest_id"),
        "contest_date": row.get("contest_date"),
        "starter_code": row.get("starter_code", ""),
    }
    return {
        "task_id": f"lcb/{row.get('question_id') or row.get('contest_id') or row.get('id')}",
        "dataset": "lcb",
        "split": split,
        "prompt": row.get("question_content") or row.get("question") or row.get("prompt"),
        "prompt_type": "stdin_stdout",
        "entry_point": None,
        "reference_code": None,
        "reference_solutions": row.get("solutions", []),
        "tests": row.get("public_test_cases") or row.get("test"),
        "test_type": "stdin_stdout",
        "difficulty": row.get("difficulty"),
        "source_url": row.get("url"),
        "metadata": metadata,
    }

def return_clean_code(file_name, base_folder):
    code_path = Path(base_folder) / file_name
    code = code_path.read_text(encoding="utf-8")
    try:
        code = remove_comments(code)
    except (IndentationError, tokenize.TokenError, ValueError):
        pass
    code = _clean_source(code)
    tree = ast.parse(code)
    if not hasattr(ast, "unparse"):
        return code
    tree = RemoveDocstrings().visit(tree)
    ast.fix_missing_locations(tree)
    clean_code = ast.unparse(tree)
    return clean_code


def avg_dicts(dicts):
    if not dicts:
        return {}
    keys = dicts[0].keys()
    avg_dict = {}
    for k in keys:
        avg_dict[k] = 0
        for d in dicts:
            avg_dict[k] += d[k]
        avg_dict[k] /= len(dicts)
    return avg_dict


def _as_reference_list(reference_solutions):
    if reference_solutions is None:
        return []
    if isinstance(reference_solutions, str):
        return [reference_solutions] if reference_solutions.strip() else []
    if isinstance(reference_solutions, tuple):
        return list(reference_solutions)
    if isinstance(reference_solutions, list):
        return reference_solutions
    return []


def _wrap_lcb_script(code):
    code = textwrap.dedent(_clean_source(code)).strip()
    if not code:
        return ""

    future_imports = []
    body_lines = []
    for line in code.splitlines():
        if line.startswith("from __future__ import "):
            future_imports.append(line)
        else:
            body_lines.append(line)

    wrapped_body = "def __lcb_solution__():\n" + textwrap.indent("\n".join(body_lines), "    ")
    if future_imports:
        return "\n".join(future_imports + ["", wrapped_body])
    return wrapped_body


def _prepare_lcb_trace_source(code, platform):
    platform = (platform or "").lower()
    if platform in {"atcoder", "codeforces"}:
        return _wrap_lcb_script(code)
    return _clean_source(textwrap.dedent(code).strip())


def get_traces_lcb(row):
    getTraces, RadonMetrics = _trace_tools()
    ref_code = _as_reference_list(row.get("reference_solutions", []))
    platform = row.get("metadata", {}).get("platform")

    ast_trace_list = []
    radon_trace_list = []

    for code in ref_code:
        if not isinstance(code, str) or not code.strip():
            continue

        trace_code = _prepare_lcb_trace_source(code, platform)
        if not trace_code:
            continue

        try:
            astTrace = getTraces(trace_code)
            radonTrace = RadonMetrics(trace_code)
            ast_trace_list.append(astTrace.getASTMetrics())
            radon_trace_list.append(radonTrace.getRadonMetrics())
        except (SyntaxError, ZeroDivisionError, ValueError):
            if platform not in {"atcoder", "codeforces"}:
                try:
                    trace_code = _wrap_lcb_script(code)
                    astTrace = getTraces(trace_code)
                    radonTrace = RadonMetrics(trace_code)
                    ast_trace_list.append(astTrace.getASTMetrics())
                    radon_trace_list.append(radonTrace.getRadonMetrics())
                except (SyntaxError, ZeroDivisionError, ValueError):
                    continue

    return avg_dicts(ast_trace_list), avg_dicts(radon_trace_list)


def _reference_solution_path(row):
    platform = row.get("platform")
    question_id = row.get("question_id")
    if not platform or not question_id:
        return None
    return (
        PROJECT_ROOT
        / "data_collection"
        / "reference_solutions"
        / "scraped"
        / str(platform).lower()
        / f"{question_id}.py"
    )

def process_one(args):
    row, normalizer, trace_extractor, split_type = args
    normalized_task = row
    if normalizer is not None:
        normalized_task = normalizer(row, split_type)

    solution_path = _reference_solution_path(row)
    try:
        if solution_path is None:
            raise FileNotFoundError("missing platform or question_id")
        clean_code = return_clean_code(solution_path.name, solution_path.parent)
        normalized_task["reference_solutions"] = [clean_code]
        normalized_task["reference_code"] = clean_code
    except (OSError, SyntaxError, tokenize.TokenError, UnicodeDecodeError, ValueError) as exc:
        task_id = normalized_task.get("task_id", row.get("question_id"))
        print(f"{task_id} reference solution skipped: {type(exc).__name__}", flush=True)
        normalized_task["reference_solutions"] = []
        normalized_task["reference_code"] = None
        
    trace_json = None
    if trace_extractor is not None:
        ast_metrics, radon_metrics = trace_extractor(normalized_task)
        trace_json = {
            "task_id": normalized_task["task_id"],
            "dataset": normalized_task["dataset"],
            "split": normalized_task["split"],
            **ast_metrics,
            **radon_metrics,
        }

    return normalized_task, trace_json

def json_converter_parallel(tasks, normalizer, trace_extractor, split_type, num_workers=8):
    if trace_extractor is not None and normalizer is None:
        raise ValueError("trace_extractor requires a normalizer so rows use the normalized schema")
    args = [(tasks[i],normalizer,trace_extractor,split_type) 
            for i in range(len(tasks))]
    normalized_tasks = []
    trace_tasks = []
    with ProcessPoolExecutor(max_workers = num_workers) as ex:
        for i,(normalized_task,trace_json) in enumerate(ex.map(process_one,args)):
            if i % 100 == 0:
                print(f"{i} done", flush=True)
            normalized_tasks.append(normalized_task)
            trace_tasks.append(trace_json)
    return normalized_tasks,trace_tasks


def _json_default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def write_jsonl(path,rows):
    os.makedirs(os.path.dirname(path),exist_ok = True)
    with open(path,"w") as f:
        for row in rows:
            f.write(json.dumps(row, default=_json_default) + "\n")

def run(task_name,normalizer = None,trace_extractor = None,split_type = "test"):
    task_folder = load_from_disk(PROJECT_ROOT / "data_collection" / "raw" / task_name)

    if isinstance(task_folder, DatasetDict):
        split_type = split_type or next(iter(task_folder.keys()))
        tasks = task_folder[split_type]
    else:
        tasks = task_folder

    normalized_tasks, trace_tasks = json_converter_parallel(tasks,normalizer,trace_extractor,split_type)
    write_jsonl(
        PROJECT_ROOT / "data_collection" / "normalized" / f"{task_name}_{split_type}.jsonl",
        normalized_tasks,
    )
    if trace_extractor is not None:
        write_jsonl(
            PROJECT_ROOT / "complexity_metrics" / "traces" / f"{task_name}_{split_type}.jsonl",
            trace_tasks,
        )


if __name__ == "__main__":
    start = time.perf_counter()
    task_name = "lcb"
    task_normalizer = normalize_lcb
    trace_extractor = get_traces_lcb
    run(task_name, task_normalizer, trace_extractor)
    end = time.perf_counter()
    print(f"Time: {end - start:.6f} s")
