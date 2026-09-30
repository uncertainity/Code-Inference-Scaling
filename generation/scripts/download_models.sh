#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

command -v hf >/dev/null || {
  echo "The Hugging Face 'hf' CLI is required." >&2
  exit 1
}

hf download Qwen/Qwen3-0.6B --local-dir generation/models/Qwen3-0.6B
hf download Qwen/Qwen3-8B --local-dir generation/models/Qwen3-8B
hf download Qwen/Qwen3-1.7B --local-dir generation/models/Qwen3-1.7B
hf download Qwen/Qwen3-4B --local-dir generation/models/Qwen3-4B
