#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

RUN_ID="${1:-scaling_law_001}"
EXPERIMENT_CONFIG="${2:-generation/configs/experiments/scaling_law_001_apps_lcb_resume.yaml}"
RUN_DIR="$ROOT_DIR/generation/runs/vllm/$RUN_ID"
LOG_DIR="$RUN_DIR/logs"
mkdir -p "$LOG_DIR"

MODELS=("Qwen3-4B" "Qwen3-8B")
PORTS=(8002 8003)
SERVER_CONFIGS=(
  "generation/configs/servers/qwen3-4b.yaml"
  "generation/configs/servers/qwen3-8b.yaml"
)

SERVER_PIDS=()
EXPERIMENT_PIDS=()

cleanup_new_processes() {
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
trap cleanup_new_processes EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

for command_name in python vllm curl setsid pgrep ps; do
  command -v "$command_name" >/dev/null || {
    echo "$command_name is required. Activate the vllm092clean environment first." >&2
    exit 1
  }
done

stop_old_server_group() {
  local config="$1"
  local launcher_pid pgid
  local -a launchers=()
  local -a pgids=()

  mapfile -t launchers < <(
    pgrep -f "python -m generation.vllm.launch_server --config $config" || true
  )

  for launcher_pid in "${launchers[@]}"; do
    pgid="$(ps -o pgid= -p "$launcher_pid" | tr -d ' ')"
    if [[ -n "$pgid" && "$pgid" != "$$" ]]; then
      pgids+=("$pgid")
    fi
  done

  if (( ${#pgids[@]} == 0 )); then
    echo "No old server group found for $config"
    return 0
  fi

  for pgid in "${pgids[@]}"; do
    echo "Stopping old server process group $pgid for $config"
    kill -- "-$pgid" 2>/dev/null || true
  done

  for _ in {1..60}; do
    local any_alive=0
    for pgid in "${pgids[@]}"; do
      if kill -0 -- "-$pgid" 2>/dev/null; then
        any_alive=1
      fi
    done
    (( any_alive == 0 )) && return 0
    sleep 2
  done

  echo "Old server group did not stop within 120 seconds: $config" >&2
  return 1
}

for config in "${SERVER_CONFIGS[@]}"; do
  stop_old_server_group "$config" || exit 1
done

for i in "${!MODELS[@]}"; do
  model="${MODELS[$i]}"
  config="${SERVER_CONFIGS[$i]}"
  log="$LOG_DIR/${model}-server-resume.log"
  echo "Starting fresh $model server with $config"
  setsid python -m generation.vllm.launch_server --config "$config" >"$log" 2>&1 &
  SERVER_PIDS+=("$!")
done

wait_for_server() {
  local model="$1"
  local port="$2"
  local pid="$3"
  local log="$4"
  local deadline=$((SECONDS + 1200))
  local response

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
    "$LOG_DIR/${MODELS[$i]}-server-resume.log" || exit 1
done

for i in "${!MODELS[@]}"; do
  model="${MODELS[$i]}"
  port="${PORTS[$i]}"
  log="$LOG_DIR/${model}-experiment-resume.log"
  echo "Resuming $model from APPS and LCB"
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
    echo "${MODELS[$i]} resume completed"
  else
    echo "${MODELS[$i]} resume failed; see $LOG_DIR/${MODELS[$i]}-experiment-resume.log" >&2
    status=1
  fi
done

if (( status == 0 )); then
  echo "4B and 8B APPS/LCB resume completed successfully: $RUN_DIR"
fi
exit "$status"
