import argparse
import io
import json
import keyword
import os
from pprint import pformat

import numpy as np
from datasets import DatasetDict, load_from_disk
import textwrap
import time
import tokenize
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _trace_tools():
    from complexity_metrics.ast_metrics import getTraces, RadonMetrics

    return getTraces, RadonMetrics


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


def normalize_mbpp(row,split = None):
    return{
        "task_id":f"mbbp/{row['task_id']}",
        "dataset":"mbpp",
        "split":split,
        "prompt":row["text"],
        "prompt_type":"function",
        "entry_point":None,
        "referrence_code":row.get("code"),
        "reference_solutions":[row["code"]] if row.get("code") else [],
        "tests":{"test_list":row.get("test_list",[]),
                 "test_setup_code":row.get("test_setup_code",[]),
                 "challenge_test_list":row.get("challenge_test_list",[])
            },
        "test_type":"assertion",
        "difficulty":None,
        "source_url":None,
        "metadata":{},
    }

def normalize_humaneval(row,split = None):
    return{
        "task_id": row['task_id'],
        "dataset":"humaneval",
        "split":split,
        "prompt":row["prompt"],
        "prompt_type":"function",
        "entry_point":row["entry_point"],
        "referrence_code":row.get("canonical_solution"),
        "reference_solutions":[row["canonical_solution"]] if row.get("canonical_solution") else [],
        "tests":row["test"],
        "test_type":"assertion",
        "difficulty":None,
        "source_url":None,
        "metadata":{},
    }

def normalize_apps(row,split = None):
    return{
        "task_id": f"apps/{row['problem_id']}",
        "dataset":"apps",
        "split":split,
        "prompt":row["question"],
        "prompt_type":"stdin_stdout",
        "entry_point":None,
        "referrence_code":None,
        "reference_solutions":row.get("solutions",[]),
        "tests":row.get("input_output"),
        "test_type":"stdin_stdout",
        "difficulty":row.get("difficulty"),
        "source_url":row.get("url"),
        "metadata":{"starter_code": row.get("starter_code", ""),},
    }
    
    
def normalize_lcb(row, split=None):
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
        "metadata": row,
    }
    

def avg_dicts(dicts):
    if not dicts:
        return {}
    ##print("dicts:",dicts)
    keys = dicts[0].keys()
    avg_dict = {}
    for k in keys:
        avg_dict[k] = 0
        for d in dicts:
            avg_dict[k] += d[k]
        avg_dict[k] /= len(dicts)
    return avg_dict


def get_traces_mbpp(row):
    getTraces, RadonMetrics = _trace_tools()
    ##ref_code = row.get("reference_solutions","")
    ##print(type(ref_code))
    ##print("Code:",ref_code)
    ast_trace_list = []
    radon_trace_list = []
    
    for code in ref_code:
        if len(code) > 0:
            code = _clean_source(code)
            astTrace = getTraces(code)
            radonTrace = RadonMetrics(code)
            idx_ast_metrics = astTrace.getASTMetrics()
            idx_radon_metrics = radonTrace.getRadonMetrics()
            ast_trace_list.append(idx_ast_metrics)
            radon_trace_list.append(idx_radon_metrics)
    
    ast_metrics = avg_dicts(ast_trace_list)
    radon_metrics = avg_dicts(radon_trace_list)
    
    return ast_metrics,radon_metrics


def get_traces_humaneval(row):
    getTraces, RadonMetrics = _trace_tools()
    ref_code = row.get("reference_solutions", "")
    prompt = row.get("prompt", "")

    ast_trace_list = []
    radon_trace_list = []

    for code in ref_code:
        if len(code) > 0:
            full_code = _clean_source(prompt + "\n" + code)

            astTrace = getTraces(full_code)
            radonTrace = RadonMetrics(full_code)

            idx_ast_metrics = astTrace.getASTMetrics()
            idx_radon_metrics = radonTrace.getRadonMetrics()

            ast_trace_list.append(idx_ast_metrics)
            radon_trace_list.append(idx_radon_metrics)

    ast_metrics = avg_dicts(ast_trace_list)
    radon_metrics = avg_dicts(radon_trace_list)

    return ast_metrics, radon_metrics
        
        
def wrap_script(code):
    code = _clean_source(textwrap.dedent(code).strip())
    return "def __apps_solution__():\n" + textwrap.indent(code, "    ")


def parse_reference_solutions(ref_code, task_id=None):
    if ref_code is None:
        return []
    if isinstance(ref_code, list):
        return ref_code
    if isinstance(ref_code, tuple):
        return list(ref_code)
    if not isinstance(ref_code, str):
        return []

    ref_code = ref_code.strip()
    if not ref_code:
        return []

    try:
        import ast as py_ast

        parsed = py_ast.literal_eval(ref_code)
    except (SyntaxError, ValueError, MemoryError, RecursionError) as exc:
        label = f" for {task_id}" if task_id is not None else ""
        print(f"Skipping malformed reference_solutions{label}: {type(exc).__name__}", flush=True)
        return []

    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, tuple):
        return list(parsed)
    if isinstance(parsed, str) and parsed.strip():
        return [parsed]
    return []
        
def get_traces_apps(row):
    getTraces, RadonMetrics = _trace_tools()
    ref_code = row.get("reference_solutions", [])
    ref_code = parse_reference_solutions(ref_code, row.get("task_id"))

    ast_trace_list = []
    radon_trace_list = []

    for code in ref_code:
        if not isinstance(code, str) or len(code.strip()) == 0:
            continue

        try:
            code = wrap_script(code)
            astTrace = getTraces(code)
            radonTrace = RadonMetrics(code)

            ast_trace_list.append(astTrace.getASTMetrics())
            radon_trace_list.append(radonTrace.getRadonMetrics())

        except SyntaxError:
            continue

    return avg_dicts(ast_trace_list), avg_dicts(radon_trace_list)


def process_one(args):
    row, normalizer, trace_extractor, split_type = args
    normalized_task = row
    if normalizer is not None:
        normalized_task = normalizer(row, split_type)
    
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

def json_converter(tasks,normalizer,trace_extractor,split_type):
    if trace_extractor is not None and normalizer is None:
        raise ValueError("trace_extractor requires a normalizer so rows use the normalized schema")

    normalized_tasks = []
    trace_tasks = []
    #for i in range(len(tasks)):
    for i in range(len(tasks)):
        if (i % 100 == 0):
            print(f"{i} done", flush=True)
        normalized_task = tasks[i]
        if normalizer is not None:
            normalized_task = normalizer(tasks[i],split_type)
        normalized_tasks.append(normalized_task)
        if trace_extractor is not None:
            
            ast_metrics,radon_metrics = trace_extractor(normalized_task)
            trace_json = {"task_id":normalized_task["task_id"], "dataset": normalized_task["dataset"],"split": normalized_task["split"],
                          **ast_metrics,**radon_metrics}
            trace_tasks.append(trace_json)
    return normalized_tasks,trace_tasks       
    ##print("normalised_tasks:",normalized_tasks)


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


def write_jsonl(path,rows):
    os.makedirs(os.path.dirname(path),exist_ok = True)
    with open(path,"w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
      
    
def run(task_name,normalizer = None,trace_extractor = None,split_type = "test"):
    task_folder = load_from_disk(PROJECT_ROOT / "data_collection" / "raw" / task_name)
    
    if isinstance(task_folder,DatasetDict):
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
    task_name = "humaneval"
    task_normalizer = normalize_humaneval
    trace_extractor = get_traces_humaneval
    run(task_name, task_normalizer, trace_extractor)
    end = time.perf_counter()
    print(f"Time: {end - start:.6f} s")
    

# task_names = ["mbpp","humaneval","apps","lcb"]
# task_normalizers = [normalize_mbpp,normalize_humaneval,normaize_apps,normalize_lcb]
# task_extractors = [get_traces_mbpp,get_traces_humaneval,get_traces_apps,get_traces_lcb]

# for i in range(len(task_names)):
#     start = time.perf_counter()
#     task_name = task_names[i]
#     task_normalizer = task_normalizers[i]
#     trace_extractor = task_extractors[i]
#     run(task_name, task_normalizer, trace_extractor)
#     end = time.perf_counter()
#     print(f"Time: {end - start:.6f} s")
