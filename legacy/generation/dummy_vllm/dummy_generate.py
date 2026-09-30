from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import yaml
import os
from prompts import DataLoader, build_prompt



ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_EXPERIMENT = ROOT_DIR / "vllm_configs" / "dummy_search.yaml"
DEFAULT_RUNS_DIR = ROOT_DIR / "runs_dummy/vllm"

async def generate_one(task,model_name,sampling_params,
                       client:httpx.AsyncClient,
                       semaphore: asyncio.Semaphore):
    prompt = build_prompt(task)
    payload = {
        "model":model_name,
        "messages":[{"role":"user","content":prompt}],
        **sampling_params
    }
    try:
        async with semaphore:
            response = await client.post("/chat/completions",json = payload)
            response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        return{
            "task_id":task["task_id"],
            "dataset":task.get("dataset"),
            "prompt":prompt,
            "prediction":"",
            "finish_reason":"error",
            "usage": None,
            "error": f"{type(exc).__name__}: {exc}",
        }
    
    return{
            "task_id":task["task_id"],
            "dataset":task.get("dataset"),
            "prompt":prompt,
            "prediction":data["choices"][0]["message"]["content"],
            "finish_reason":data["choices"][0]["finish_reason"],
            "usage": data.get("usage"),
        }
    
async def run_inference(tasks,base_url,model_name,sampling_params,concurrency):
    semaphore = asyncio.Semaphore(concurrency)
    timeout = httpx.Timeout(connect = 30.0, read = 1800.0, write = 30.0, pool = 30.0)
    limits = httpx.Limits(
        max_connections=concurrency,
        max_keepalive_connections=concurrency,
    )
    async with httpx.AsyncClient(
        base_url=base_url.rstrip("/") + "/v1",
        timeout=timeout,
        limits=limits,
    ) as client:
        jobs = [
            generate_one(task, model_name, sampling_params, client, semaphore)
            for task in tasks
        ]
        return await asyncio.gather(*jobs)


def load_experiment(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        experiment = yaml.safe_load(file)
    if not isinstance(experiment, dict):
        raise ValueError(f"Experiment config must be a mapping: {path}")
    return experiment


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")

## Sampling param path
## task path

## vllm config path: DEFAULT_EXPERIMENTS/vllm_configs/dummy_search.yaml
## default runs dir: ROOT_DIR / "runs_dummy/vllm/models/model_name"

def run_dummy(experiment_path,model_name,base_url):
    experiment = load_experiment(experiment_path)
    task_paths = experiment["task_paths"]
    sampling_configs = experiment["sampling_configs"]
    batch_size = int(experiment.get("batch_size", 1000))
    concurrency = int(experiment.get("concurrency", 64))

    model_dir = DEFAULT_RUNS_DIR / "models" / model_name
    ##os.makedir(model_dir,exists_ok = True)
    for config_name,sampling_params in sampling_configs.items():
        config_dir = model_dir / config_name
        print(sampling_params)
        print(config_name)
        for task_path in task_paths:
            loader = DataLoader(task_path)
            all_results = []
            for batch in loader.loader(batch_size):
                results = asyncio.run(
                    run_inference(
                        batch, base_url, model_name, sampling_params, concurrency
                    )
                )
                all_results.extend(results)

            dataset_name = Path(task_path).stem.removesuffix("_subset")
            output_path = config_dir / f"{dataset_name}_generations.jsonl"
            write_jsonl(output_path, all_results)
            
if __name__ == "__main__":
    port = os.environ.get("PORT", "8000")
    model_name = os.environ.get("MODEL_NAME", "Qwen3-0.6B")
    run_dummy(experiment_path = DEFAULT_EXPERIMENT,model_name = model_name,base_url = f"http://127.0.0.1:{port}")
    

    
