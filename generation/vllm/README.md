# vLLM experiment workflow

Run commands from the repository root.

## Start the four subset-search servers

Use one terminal or screen session per server:

```bash
python -m generation.vllm.launch_server --config generation/configs/servers/qwen3-0.6b.yaml
python -m generation.vllm.launch_server --config generation/configs/servers/qwen3-1.7b.yaml
python -m generation.vllm.launch_server --config generation/configs/servers/qwen3-4b.yaml
python -m generation.vllm.launch_server --config generation/configs/servers/qwen3-8b.yaml
```

The checked-in mapping is GPU/port `4/8000`, `5/8001`, `6/8002`, and `7/8003`.
Edit the server YAMLs when using a machine with a different GPU layout.

## Run the subset sampling search

Use the same run ID for all four models:

```bash
python -m generation.vllm.generate --model Qwen3-0.6B --base-url http://localhost:8000 --run-id qwen3_sampling_search_001
python -m generation.vllm.generate --model Qwen3-1.7B --base-url http://localhost:8001 --run-id qwen3_sampling_search_001
python -m generation.vllm.generate --model Qwen3-4B --base-url http://localhost:8002 --run-id qwen3_sampling_search_001
python -m generation.vllm.generate --model Qwen3-8B --base-url http://localhost:8003 --run-id qwen3_sampling_search_001
```

Outputs are written under:

```text
generation/runs/vllm/<run-id>/models/<model>/<sampling-config>/
```

Each model directory contains a run manifest. Each sampling directory contains
the exact sampling parameters and one generations JSONL file per dataset.

## Run all four models together

After activating the vLLM environment, the orchestration script starts all four
servers, waits for readiness, runs all four searches concurrently, and shuts
the servers down when the searches finish:

```bash
bash generation/vllm/run_four_model_search.sh qwen3_sampling_search_001
```

An alternative experiment YAML can be passed as the second argument:

```bash
bash generation/vllm/run_four_model_search.sh \
  qwen3_sampling_search_001 \
  generation/configs/experiments/sampling_search.yaml
```

Server and experiment logs are stored in `generation/runs/vllm/<run-id>/logs/`.
