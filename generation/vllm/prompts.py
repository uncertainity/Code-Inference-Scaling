import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

def build_function_prompt(task,template):
    if template == "simple":
        return f"""You are an expert Python programmer.

    {task["prompt"]}

    Return only the Python function.
    Do not include explanations.
    Do not include:
    - Markdown code fences
    - Explanations
    - Comments outside the program
    - Alternative solutions
    """
    elif template == "official":
        raise ValueError("No official prompt found.")
    

def build_stdin_stdout_prompt(task,template):
    if template == "simple":
        return f"""You are an expert competitive programmer.

    {task["prompt"]}

    Return only a complete Python program.
    Do not include explanations.
    Do not include:
    - Markdown code fences
    - Explanations
    - Comments outside the program
    - Alternative solutions
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


class DataLoader:
    
    def __init__(self, task_name):
        task_path = Path(task_name)
        self.path = task_path if task_path.is_absolute() else BASE_DIR / task_path
        print(f"path:{self.path}")
        
    def loader(self,batch_size = 32):
        batch = []
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                batch.append(json.loads(line))
                if len(batch) == batch_size:
                    yield batch
                    batch = []
        if batch:
            yield batch
    
