# Stage 4: vLLM generation

This stage serves local Qwen3 checkpoints with vLLM and sends the fair
benchmark prompts through the OpenAI-compatible chat-completions endpoint.

## Layout

- `configs/servers/`: model, GPU, port, and vLLM serving settings
- `configs/experiments/`: task paths, concurrency, and sampling budgets
- `models/`: local model snapshots (not committed)
- `vllm/`: server launcher, prompt builder, async client, and orchestration
- `runs/`: manifests, exact sampling configs, logs, and generated JSONL

## Single-model run

From the repository root:

```bash
python -m generation.vllm.launch_server \
  --config generation/configs/servers/qwen3-0.6b.yaml

python -m generation.vllm.generate \
  --model Qwen3-0.6B \
  --base-url http://127.0.0.1:8000 \
  --run-id example_run \
  --experiment generation/configs/experiments/scaling_law_001.yaml
```

The generator batches JSONL lazily, bounds concurrent HTTP requests with an
async semaphore, records request errors as rows instead of dropping tasks, and
writes a manifest plus the exact sampling parameters beside each output.

To launch all four configured models, use:

```bash
bash generation/vllm/run_four_model_search.sh example_run \
  generation/configs/experiments/scaling_law_001.yaml
```

See [`vllm/README.md`](vllm/README.md) for port mappings and operational
details. vLLM itself must be installed separately for the machine's CUDA and
PyTorch versions.

