#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

LOG_DIR="$ROOT_DIR/runs_dummy/vllm/logs"
mkdir -p "$LOG_DIR"

# MODELS=("Qwen3-0.6B" "Qwen3-1.7B")
# PORTS=(8000 8001)
# SERVER_CONFIGS=(
#   "configs/servers/qwen3-0.6b.yaml"
#   "configs/servers/qwen3-1.7b.yaml"
# )

MODELS=("Qwen3-0.6B")
PORTS=(8000)
SERVER_CONFIGS=(
  "configs/servers/qwen3-0.6b.yaml"
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

  # Give vLLM a moment to stop, then remove any surviving process groups.
  sleep 5
  for pid in "${SERVER_PIDS[@]}"; do
    kill -KILL -- "-$pid" 2>/dev/null || true
  done

  wait 2>/dev/null || true
  exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

command -v python >/dev/null || {
  echo "python is not available. Activate the vLLM environment first." >&2
  exit 1
}
command -v vllm >/dev/null || {
  echo "vllm is not available. Activate the vLLM environment first." >&2
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

for i in "${!MODELS[@]}"; do
  model="${MODELS[$i]}"
  config="${SERVER_CONFIGS[$i]}"
  echo "Starting $model"
  setsid python -m inference.vllm.launch_server --config "$config" \
    >"$LOG_DIR/${model}-server.log" 2>&1 &
  SERVER_PIDS+=("$!")
done

wait_for_server() {
  local model="$1"
  local port="$2"
  local pid="$3"
  local deadline=$((SECONDS + 1200))

  while (( SECONDS < deadline )); do
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "$model server exited. See $LOG_DIR/${model}-server.log" >&2
      return 1
    fi

    response="$(curl --noproxy '*' -fsS "http://127.0.0.1:$port/v1/models" 2>/dev/null || true)"
    if [[ "$response" == *"\"id\":\"$model\""* ]]; then
      echo "$model is ready on port $port"
      return 0
    fi
    sleep 5
  done

  echo "Timed out waiting for $model" >&2
  return 1
}

for i in "${!MODELS[@]}"; do
  wait_for_server "${MODELS[$i]}" "${PORTS[$i]}" "${SERVER_PIDS[$i]}" || exit 1
done

for i in "${!MODELS[@]}"; do
  echo "Starting dummy experiment for ${MODELS[$i]}"
  MODEL_NAME="${MODELS[$i]}" PORT="${PORTS[$i]}" \
    python inference/dummy_vllm/dummy_generate.py &
  EXPERIMENT_PIDS+=("$!")
done

status=0
for i in "${!EXPERIMENT_PIDS[@]}"; do
  if wait "${EXPERIMENT_PIDS[$i]}"; then
    echo "${MODELS[$i]} experiment completed"
  else
    echo "${MODELS[$i]} experiment failed" >&2
    status=1
  fi
done

exit "$status"

