#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

RUN_ID="${1:-qwen3_sampling_search_$(date +%Y%m%d_%H%M%S)}"
EXPERIMENT_CONFIG="${2:-generation/configs/experiments/sampling_search.yaml}"
RUN_DIR="$ROOT_DIR/generation/runs/vllm/$RUN_ID"
LOG_DIR="$RUN_DIR/logs"
mkdir -p "$LOG_DIR"

MODELS=("Qwen3-0.6B" "Qwen3-1.7B" "Qwen3-4B" "Qwen3-8B")
PORTS=(8000 8001 8002 8003)
SERVER_CONFIGS=(
  "generation/configs/servers/qwen3-0.6b.yaml"
  "generation/configs/servers/qwen3-1.7b.yaml"
  "generation/configs/servers/qwen3-4b.yaml"
  "generation/configs/servers/qwen3-8b.yaml"
)

SERVER_PIDS=()
EXPERIMENT_PIDS=()

cleanup() {
  local status=$?
  trap - EXIT INT TERM

  for pid in "${EXPERIMENT_PIDS[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
  done

  for pid in "${SERVER_PIDS[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill -- "-$pid" 2>/dev/null || kill "$pid" 2>/dev/null || true
    fi
  done

  wait 2>/dev/null || true
  exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

command -v python >/dev/null || {
  echo "python is not available. Activate the vllm092clean environment first." >&2
  exit 1
}
command -v vllm >/dev/null || {
  echo "vllm is not available. Activate the vllm092clean environment first." >&2
  exit 1
}
command -v curl >/dev/null || {
  echo "curl is required for server readiness checks." >&2
  exit 1
}
command -v setsid >/dev/null || {
  echo "setsid is required to manage the server process groups." >&2
  exit 1
}

for port in "${PORTS[@]}"; do
  if ss -ltn "sport = :$port" | tail -n +2 | grep -q .; then
    echo "Port $port is already in use. Stop that process before starting this run." >&2
    exit 1
  fi
done

echo "Run ID: $RUN_ID"
echo "Experiment: $EXPERIMENT_CONFIG"
echo "Logs: $LOG_DIR"

for i in "${!MODELS[@]}"; do
  model="${MODELS[$i]}"
  config="${SERVER_CONFIGS[$i]}"
  log="$LOG_DIR/${model}-server.log"
  echo "Starting $model with $config"
  setsid python -m generation.vllm.launch_server --config "$config" >"$log" 2>&1 &
  SERVER_PIDS+=("$!")
done

wait_for_server() {
  local model="$1"
  local port="$2"
  local pid="$3"
  local log="$4"
  local deadline=$((SECONDS + 1200))

  while (( SECONDS < deadline )); do
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "$model server exited before becoming ready. See $log" >&2
      return 1
    fi

    response="$(curl --noproxy '*' -fsS "http://127.0.0.1:$port/v1/models" 2>/dev/null || true)"
    if [[ "$response" == *"\"id\":\"$model\""* ]]; then
      echo "$model is ready on port $port"
      return 0
    fi
    sleep 5
  done

  echo "Timed out waiting for $model on port $port. See $log" >&2
  return 1
}

for i in "${!MODELS[@]}"; do
  wait_for_server \
    "${MODELS[$i]}" \
    "${PORTS[$i]}" \
    "${SERVER_PIDS[$i]}" \
    "$LOG_DIR/${MODELS[$i]}-server.log" || exit 1
done

for i in "${!MODELS[@]}"; do
  model="${MODELS[$i]}"
  port="${PORTS[$i]}"
  log="$LOG_DIR/${model}-experiment.log"
  echo "Starting subset search for $model"
  python -m generation.vllm.generate \
    --model "$model" \
    --base-url "http://127.0.0.1:$port" \
    --run-id "$RUN_ID" \
    --experiment "$EXPERIMENT_CONFIG" >"$log" 2>&1 &
  EXPERIMENT_PIDS+=("$!")
done

status=0
for i in "${!EXPERIMENT_PIDS[@]}"; do
  if wait "${EXPERIMENT_PIDS[$i]}"; then
    echo "${MODELS[$i]} experiment completed"
  else
    echo "${MODELS[$i]} experiment failed; see $LOG_DIR/${MODELS[$i]}-experiment.log" >&2
    status=1
  fi
done

if (( status == 0 )); then
  echo "All experiments completed successfully: $RUN_DIR"
fi
exit "$status"
