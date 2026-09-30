from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import yaml

from .prompts import DataLoader, build_prompt


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_EXPERIMENT = ROOT_DIR / "generation/configs/experiments/sampling_search.yaml"
DEFAULT_RUNS_DIR = ROOT_DIR / "generation/runs/vllm"


async def generate_one(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    task: dict[str, Any],
    model_name: str,
    sampling_params: dict[str, Any],
) -> dict[str, Any]:
    prompt = build_prompt(task)
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        **sampling_params,
    }

    try:
        async with semaphore:
            response = await client.post("/chat/completions", json=payload)
            response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        return {
            "task_id": task["task_id"],
            "dataset": task.get("dataset"),
            "prompt": prompt,
            "prediction": "",
            "finish_reason": "error",
            "usage": None,
            "error": f"{type(exc).__name__}: {exc}",
        }

    return {
        "task_id": task["task_id"],
        "dataset": task.get("dataset"),
        "prompt": prompt,
        "prediction": data["choices"][0]["message"]["content"],
        "finish_reason": data["choices"][0]["finish_reason"],
        "usage": data.get("usage"),
    }


async def run_inference(
    tasks: list[dict[str, Any]],
    base_url: str,
    model_name: str,
    sampling_params: dict[str, Any],
    concurrency: int,
) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency)
    timeout = httpx.Timeout(connect=30.0, read=3600.0, write=30.0, pool=30.0)
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
            generate_one(client, semaphore, task, model_name, sampling_params)
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


def run_config_search(
    experiment_path: Path,
    run_id: str,
    model_name: str,
    base_url: str,
) -> None:
    experiment = load_experiment(experiment_path)
    task_paths = experiment["task_paths"]
    sampling_configs = experiment["sampling_configs"]
    batch_size = int(experiment.get("batch_size", 1000))
    concurrency = int(experiment.get("concurrency", 64))

    model_dir = DEFAULT_RUNS_DIR / run_id / "models" / model_name
    model_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "run_id": run_id,
        "created_at": datetime.now().astimezone().isoformat(),
        "protocol": experiment.get("protocol", "solve_at_1"),
        "model": model_name,
        "base_url": base_url,
        "experiment_config": str(experiment_path.resolve()),
        "task_paths": task_paths,
        "sampling_configs": sampling_configs,
    }
    with (model_dir / "manifest.json").open("w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2, ensure_ascii=False)

    for config_name, sampling_params in sampling_configs.items():
        config_dir = model_dir / config_name
        config_dir.mkdir(parents=True, exist_ok=True)
        with (config_dir / "config.json").open("w", encoding="utf-8") as file:
            json.dump(sampling_params, file, indent=2, ensure_ascii=False)

        for task_path in task_paths:
            loader = DataLoader(task_path)
            all_results = []
            for batch in loader.loader(batch_size):
                results = asyncio.run(
                    run_inference(
                        batch,
                        base_url,
                        model_name,
                        sampling_params,
                        concurrency,
                    )
                )
                all_results.extend(results)

            dataset_name = Path(task_path).stem.removesuffix("_subset")
            for result in all_results:
                result.update(
                    {
                        "run_id": run_id,
                        "model": model_name,
                        "config_name": config_name,
                        "protocol": experiment.get("protocol", "solve_at_1"),
                    }
                )
            output_path = config_dir / f"{dataset_name}_generations.jsonl"
            write_jsonl(output_path, all_results)
            print(f"Wrote {len(all_results)} results to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a vLLM sampling search")
    parser.add_argument("--model", required=True, help="vLLM served model name")
    parser.add_argument("--base-url", required=True, help="Server URL, e.g. http://localhost:8002")
    parser.add_argument("--run-id", required=True, help="Shared experiment run identifier")
    parser.add_argument("--experiment", type=Path, default=DEFAULT_EXPERIMENT)
    args = parser.parse_args()
    run_config_search(args.experiment, args.run_id, args.model, args.base_url)


if __name__ == "__main__":
    main()
