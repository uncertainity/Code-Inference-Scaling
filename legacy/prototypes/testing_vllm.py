from dataloader import *
import asyncio
import json
from pathlib import Path
from typing import Any
import httpx

VLLM_URL = "http://localhost:8000/v1/chat/completions"
MODEL_NAME = "Qwen3-4B"

TASK_LIST = [
    "fair_data/test_results/humaneval_subset.jsonl",
    "fair_data/test_results/mbpp_subset.jsonl",
    "fair_data/test_results/apps_subset.jsonl",
    "fair_data/test_results/lcb_subset.jsonl",
]

CONFIG_EXP_DIR = Path(__file__).resolve().parent / "fair_data/config_exp"

SAMPLING_CONFIGS = {
    "no_thinking_greedy": {
        "temperature": 0.0,
        "max_tokens": 4096,
        "chat_template_kwargs": {"enable_thinking": False},
    },
    "no_thinking_sampled": {
        "temperature": 0.2,
        "top_p": 0.95,
        "repetition_penalty": 1.05,
        "max_tokens": 4096,
        "chat_template_kwargs": {"enable_thinking": False},
    },
    "thinking_greedy": {
        "temperature": 0.0,
        "max_tokens": 8192,
        "chat_template_kwargs": {"enable_thinking": True},
    },
    "thinking_sampled": {
        "temperature": 0.2,
        "top_p": 0.95,
        "repetition_penalty": 1.05,
        "max_tokens": 8192,
        "chat_template_kwargs": {"enable_thinking": True},
    },
    "no_thinking_qwen_recommended": {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 20,
        "min_p": 0.0,
        "max_tokens": 4096,
        "chat_template_kwargs": {"enable_thinking": False},
    },
    "thinking_qwen_recommended": {
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20,
        "min_p": 0.0,
        "max_tokens": 8192,
        "chat_template_kwargs": {"enable_thinking": True},
    },
    "thinking_qwen_presence_penalty": {
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20,
        "min_p": 0.0,
        "presence_penalty": 1.0,
        "max_tokens": 8192,
        "chat_template_kwargs": {"enable_thinking": True},
    },
}


# Maximum number of simultaneously active HTTP requests.
CONCURRENCY = 64

async def generate_one(
    sampling_params: dict[str, Any],
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    task: dict[str, Any],
):
    prompt = build_prompt(task)
    payload = {
    "model": MODEL_NAME,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
        **sampling_params,
    }
    async with semaphore:
        response = await client.post(VLLM_URL,json = payload)
        response.raise_for_status()
    data = response.json()
    
    return {
        "task_id": task["task_id"],
        "prompt": prompt,
        "prediction": data["choices"][0]["message"]["content"],
        "finish_reason": data["choices"][0]["finish_reason"],
        "usage": data.get("usage"),
    }
        
        
async def run_inference(
    tasks: list[dict[str, Any]],
    sampling_params: dict[str, Any],
    concurrency: int,
) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency)
    timeout = httpx.Timeout(
        connect=30.0,
        read=600.0,
        write=30.0,
        pool=30.0,
    )

    limits = httpx.Limits(
        max_connections=concurrency,
        max_keepalive_connections=concurrency,
    )

    async with httpx.AsyncClient(
        timeout=timeout,
        limits=limits,
    ) as client:
        jobs = [
            generate_one(sampling_params, client, semaphore, task)
            for task in tasks
        ]

        results = await asyncio.gather(*jobs)

    return results


def run_config_search(
    task_list=TASK_LIST,
    sampling_configs=SAMPLING_CONFIGS,
    batch_size=1000,
    concurrency=CONCURRENCY,
):
    for config_name, sampling_params in sampling_configs.items():
        config_dir = CONFIG_EXP_DIR / config_name
        config_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "model": MODEL_NAME,
            "sampling_params": sampling_params,
        }
        with (config_dir / "config.json").open("w", encoding="utf-8") as file:
            json.dump(manifest, file, indent=2, ensure_ascii=False)

        for task_name in task_list:
            batch_loader = DataLoader(task_name)
            all_results = []
            for batch in batch_loader.loader(batch_size):
                results = asyncio.run(
                    run_inference(batch, sampling_params, concurrency)
                )
                all_results.extend(results)

            dataset_name = Path(task_name).stem.removesuffix("_subset")
            output_file = config_dir / f"{dataset_name}_results.jsonl"
            with output_file.open("w", encoding="utf-8") as file:
                for result in all_results:
                    result["config_name"] = config_name
                    file.write(json.dumps(result, ensure_ascii=False) + "\n")

            print(f"Wrote {len(all_results)} results to {output_file}")
        


if __name__ == "__main__":
    run_config_search()
