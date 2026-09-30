import argparse
import json
from pprint import pformat

import numpy as np
from datasets import DatasetDict, load_from_disk
from ast_python import getTraces, RadonMetrics
import textwrap

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
    
   
    
    
def build_function_prompt(task,template):
    if template == "simple":
        return f"""You are an expert Python programmer.

    {task["prompt"]}

    Return only the Python function.
    Do not include explanations.
    """
    elif template == "official":
        raise ValueError("No official prompt found.")
    

def build_stdin_stdout_prompt(task,template):
    if template == "simple":
        return f"""You are an expert competitive programmer.

    {task["prompt"]}

    Return only a complete Python program.
    Do not include explanations.
    """
    elif template == "official":
        raise ValueError("No official prompt found.")
    

def build_prompt(task,template = "simple"):
    #print("Task type:",type(task))
    #print("Task:",task)
    if task["prompt_type"] == "stdin_stdout":
        prompts = build_stdin_stdout_prompt(task,template)
    elif task["prompt_type"] == "function":
        prompts = build_function_prompt(task,template)
    else:
        raise ValueError("Task Type must be either stdin_stdout(program) or function")
    return prompts


class TaskLoader:
    def __init__(self,tasks,normalizer = None,split_type = "test"):
        self.tasks = tasks
        self.normalizer = normalizer
        self.split_type = split_type
    
    def batches(self,batch_size):
        for i in range(0,len(self.tasks),batch_size):
            raw_batch = [self.tasks[j] for j in range(i,min(i+batch_size,len(self.tasks)))]
            if self.normalizer is not None:
                normaized_batch = []
                for row in raw_batch:
                    normalized_row = self.normalizer(row,self.split_type)
                    get_traces(normalized_row)
                    normalized_batch.append(normalized_row)    
                yield normalized_batch
            else:
                yield raw_batch


def get_dataloader(task_name,normalizer = None,split_type = "test",batch_size = 2):
    
    task_folder = load_from_disk("data/" + task_name)
    
    if isinstance(task_folder,DatasetDict):
        split_type = split_type or next(iter(task_folder.keys()))
        tasks = task_folder[split_type]
    else:
        tasks = task_folder
    #print(tasks)
    task_loader = TaskLoader(tasks,normalizer,split_type)
    for batch in task_loader.batches(batch_size):
        prompts = [build_prompt(t) for t in batch]
        ##print(prompts)
    print(f"Finished checking {task_name}")


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
    ref_code = row.get("reference_solutions","")
    ##print(type(ref_code))
    print("Code:",ref_code)
    ast_trace_list = []
    radon_trace_list = []
    
    for code in ref_code:
        if len(code) > 0:
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
    ref_code = row.get("reference_solutions", "")
    prompt = row.get("prompt", "")

    ast_trace_list = []
    radon_trace_list = []

    for code in ref_code:
        if len(code) > 0:
            full_code = prompt + "\n" + code

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
    code = textwrap.dedent(code).strip()
    return "def __apps_solution__():\n" + textwrap.indent(code, "    ")
        
def get_traces_apps(row):
    ref_code = row.get("reference_solutions", [])

    # If accidentally stored as a stringified list, parse it back
    if isinstance(ref_code, str):
        import ast as py_ast
        ref_code = py_ast.literal_eval(ref_code)

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


     
def rough_run(task_name,normalizer = None,split_type = "test"):
    task_folder = load_from_disk("data/" + task_name)
    
    if isinstance(task_folder,DatasetDict):
        split_type = split_type or next(iter(task_folder.keys()))
        tasks = task_folder[split_type]
    else:
        tasks = task_folder
    
    len_tasks = len(tasks)
    #ast_metrics = []
    #radon_metrics = []
    
    for i in range(10):
        print("--" * 10)
        print(f"i:{i}")
        row = tasks[i]
        normalized_row = normalizer(row,split_type)
        ast_row,radon_row = get_traces_apps(normalized_row)
        print("AST Row:",ast_row)
        print("Radon Row:",radon_row)
        #ast_metrics += ast_row
        #radon_metrics += radon_row
        #return ast_row,radon_row
 
    
task_name = "apps"
task_normalizer = normalize_apps
rough_run(task_name,task_normalizer)




            

# get_dataloader(task_name,task_normalizer)
 
# task_name = "humaneval"
# task_normalizer = normalize_humaneval
# get_dataloader(task_name,task_normalizer)

# task_name = "apps"
# task_normalizer = normalize_apps
# get_dataloader(task_name,task_normalizer)

# task_name = "lcb"
# task_normalizer = normalize_lcb
# get_dataloader(task_name,task_normalizer)




