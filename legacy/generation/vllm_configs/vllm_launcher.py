import os
from pathlib import Path
import yaml
import subprocess

config_path = Path(__file__).with_name("Qwen3-4B.yaml")
env = os.environ.copy()

with config_path.open("r") as file:
    config = yaml.safe_load(file)

env["CUDA_VISIBLE_DEVICES"] = config.pop("gpu")
command = ["vllm","serve",config.pop("model")]

for key,value in config.items():
    option = "--" + key.replace("_","-")
    if isinstance(value,bool):
        if value:
            command.append(option)
    else:
        command.extend([option,str(value)])

subprocess.run(command, env=env, check=True)
