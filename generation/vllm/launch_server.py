import argparse
import os
from pathlib import Path
import subprocess

import yaml


ROOT_DIR = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch a vLLM server from YAML")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()

    config_path = args.config.resolve()
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    config = dict(config)
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(config.pop("gpu"))
    model = config.pop("model")
    command = ["vllm", "serve", str(model)]

    for key, value in config.items():
        option = "--" + key.replace("_", "-")
        if isinstance(value, bool):
            if value:
                command.append(option)
        else:
            command.extend([option, str(value)])

    print("Launching:", " ".join(command))
    subprocess.run(command, env=env, cwd=ROOT_DIR, check=True)


if __name__ == "__main__":
    main()
