#!/usr/bin/env bash
set -euo pipefail

export PATH="/data1/sandesh/.conda/envs/vllm092clean/bin:$PATH"

cd /data1/sandesh/arka/Compression_Law
exec bash inference/dummy_vllm/run_dummy_2.sh
