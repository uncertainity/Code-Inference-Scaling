#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

RUN_ID="${1:-scaling_law_001}"
EXPERIMENT_CONFIG="${2:-generation/configs/experiments/scaling_law_001_apps_lcb_resume.yaml}"
RUN_DIR="$ROOT_DIR/generation/runs/vllm/$RUN_ID"
LOG_DIR="$RUN_DIR/logs"
MODEL="Qwen3-1.7B"
PORT=8001
SERVER_CONFIG="generation/configs/servers/qwen3-1.7b.yaml"
SERVER_LOG="$LOG_DIR/$MODEL-server-resume.log"
EXPERIMENT_LOG="$LOG_DIR/$MODEL-experiment-resume.log"

mkdir -p "$LOG_DIR"

SERVER_PID=""
EXPERIMENT_PID=""

cleanup_new_processes() {
  local status=$?
  trap - EXIT INT TERM

  if [[ -n "$EXPERIMENT_PID" ]] && kill -0 "$EXPERIMENT_PID" 2>/dev/null; then
    kill "$EXPERIMENT_PID" 2>/dev/null || true
  fi

  if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill -- "-$SERVER_PID" 2>/dev/null || kill "$SERVER_PID" 2>/dev/null || true
  fi

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
  local launcher_pid pgid
  local -a launchers=()
  local -a pgids=()

  mapfile -t launchers < <(
    pgrep -f "python -m generation.vllm.launch_server --config $SERVER_CONFIG" || true
  )

  for launcher_pid in "${launchers[@]}"; do
    pgid="$(ps -o pgid= -p "$launcher_pid" | tr -d ' ')"
    if [[ -n "$pgid" && "$pgid" != "$$" ]]; then
      pgids+=("$pgid")
    fi
  done

  if (( ${#pgids[@]} == 0 )); then
    echo "No old server group found for $SERVER_CONFIG"
    return 0
  fi

  for pgid in "${pgids[@]}"; do
    echo "Stopping old server process group $pgid for $SERVER_CONFIG"
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

  echo "Old server group did not stop within 120 seconds: $SERVER_CONFIG" >&2
  return 1
}

stop_old_server_group || exit 1

echo "Starting fresh $MODEL server with $SERVER_CONFIG"
setsid python -m generation.vllm.launch_server --config "$SERVER_CONFIG" \
  >"$SERVER_LOG" 2>&1 &
SERVER_PID="$!"

wait_for_server() {
  local deadline=$((SECONDS + 1200))
  local response

  while (( SECONDS < deadline )); do
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
      echo "$MODEL server exited before becoming ready. See $SERVER_LOG" >&2
      return 1
    fi

    response="$(curl --noproxy '*' -fsS "http://127.0.0.1:$PORT/v1/models" 2>/dev/null || true)"
    if [[ "$response" == *"\"id\":\"$MODEL\""* ]]; then
      echo "$MODEL is ready on port $PORT"
      return 0
    fi
    sleep 5
  done

  echo "Timed out waiting for $MODEL on port $PORT. See $SERVER_LOG" >&2
  return 1
}

wait_for_server || exit 1

echo "Resuming $MODEL from APPS and LCB"
python -m generation.vllm.generate \
  --model "$MODEL" \
  --base-url "http://127.0.0.1:$PORT" \
  --run-id "$RUN_ID" \
  --experiment "$EXPERIMENT_CONFIG" >"$EXPERIMENT_LOG" 2>&1 &
EXPERIMENT_PID="$!"

if wait "$EXPERIMENT_PID"; then
  EXPERIMENT_PID=""
  echo "$MODEL APPS/LCB resume completed successfully: $RUN_DIR"
else
  status=$?
  EXPERIMENT_PID=""
  echo "$MODEL resume failed; see $EXPERIMENT_LOG" >&2
  exit "$status"
fi
