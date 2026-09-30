import argparse
import logging
import subprocess
import time
from pathlib import Path

import psutil


# MODELS = ["Qwen3-0.6B", "Qwen3-1.7B", "Qwen3-4B", "Qwen3-8B"]
MODELS = ["Qwen3-8B"]
RUN_ID = "scaling_law_001"
LOG_PATHS = {
    "Qwen3-8B": Path(
        "/data1/sandesh/arka/Compression_Law/"
        "runs/vllm/scaling_law_001/logs/Qwen3-8B-server-resume.log"
    ),
}

# "Qwen3-0.6B": Path(
#         "/data1/sandesh/arka/Compression_Law/"
#         "runs/vllm/scaling_law_001/logs/Qwen3-0.6B-server.log"
#     ),


def find_pid(model: str, run_id: str):
    pattern = (
        rf"inference\.vllm\.generate.*"
        rf"--model {model}.*"
        rf"--run-id {run_id}"
    )
    result = subprocess.run(
        ["pgrep", "-f", pattern],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 1:
        return None
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "pgrep failed")

    pids = [int(pid) for pid in result.stdout.split()]
    if len(pids) > 1:
        raise RuntimeError(f"Multiple matching processes: {pids}")
    return pids[0]


def get_gpu_percent(model: str):
    """Return utilization of the GPU serving model, or None if unavailable."""
    try:
        compute_result = subprocess.run(
            [
                "nvidia-smi",
                "--query-compute-apps=gpu_uuid,pid",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        gpu_result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=uuid,utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        compute_gpu_by_pid = {}
        for line in compute_result.stdout.splitlines():
            gpu_uuid, pid_text = (part.strip() for part in line.split(",", 1))
            compute_gpu_by_pid[int(pid_text)] = gpu_uuid

        utilization_by_gpu = {}
        for line in gpu_result.stdout.splitlines():
            gpu_uuid, percent_text = (part.strip() for part in line.split(",", 1))
            utilization_by_gpu[gpu_uuid] = float(percent_text)

        server_marker = f"--served-model-name {model}"
        for process in psutil.process_iter(["cmdline"]):
            try:
                command = " ".join(process.info["cmdline"] or [])
                if "vllm serve" not in command or server_marker not in command:
                    continue

                server_pids = {process.pid}
                server_pids.update(child.pid for child in process.children(recursive=True))
                for server_pid in server_pids:
                    gpu_uuid = compute_gpu_by_pid.get(server_pid)
                    if gpu_uuid is not None:
                        return utilization_by_gpu.get(gpu_uuid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        pass

    return None


def get_status(pid, log_path: Path, model: str, stale_seconds: int):
    now = time.time()
    pid_alive = pid is not None and psutil.pid_exists(pid)
    log_exists = log_path.exists()
    log_age = now - log_path.stat().st_mtime if log_exists else None
    cpu_percent = None
    memory_mb = None

    if pid_alive:
        try:
            process = psutil.Process(pid)
            cpu_percent = process.cpu_percent(interval=0.2)
            memory_mb = process.memory_info().rss / (1024**2)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pid_alive = False

    reasons = []
    if not pid_alive:
        reasons.append("generator process is not running")
    if not log_exists:
        reasons.append("server log does not exist")
    elif log_age > stale_seconds:
        reasons.append(f"server log is stale ({log_age:.0f}s old)")

    return {
        "healthy": not reasons,
        "reasons": reasons,
        "pid": pid,
        "pid_alive": pid_alive,
        "log_exists": log_exists,
        "log_age_seconds": log_age,
        "cpu_percent": cpu_percent,
        "memory_mb": memory_mb,
        "gpu_percent": get_gpu_percent(model),
    }


def format_optional(value, suffix="", precision=1):
    if value is None:
        return "n/a"
    return f"{value:.{precision}f}{suffix}"


def configure_logging(log_file: Path):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file)],
        force=True,
    )

def send_notification(message: str):
    subprocess.run(
        [
            "curl",
            "-fsS",
            "-H",
            "Title: Scaling-law monitor",
            "-H",
            "Priority: high",
            "-d",
            message,
            "https://ntfy.sh/arka-scaling-law-001",
        ],
        check=False,
        timeout=15,
    )

def check_all_models(run_id: str, stale_seconds: int):
    statuses = {}
    for model in MODELS:
        try:
            pid = find_pid(model, run_id)
            status = get_status(pid, LOG_PATHS[model], model, stale_seconds)
        except Exception as error:
            logging.exception("model=%s checker_error=%s", model, error)
            statuses[model] = {"healthy": False, "reasons": [str(error)]}
            continue

        statuses[model] = status
        if not status["healthy"]:
            send_notification(
                f"{model} is unhealthy: "
                + "; ".join(status["reasons"])
            )
        level = logging.INFO if status["healthy"] else logging.ERROR
        detail = "ok" if status["healthy"] else "; ".join(status["reasons"])
        logging.log(
            level,
            (
                "model=%s health=%s pid=%s log_age=%s cpu=%s "
                "memory=%s gpu=%s detail=%s"
            ),
            model,
            "healthy" if status["healthy"] else "unhealthy",
            status["pid"] if status["pid"] is not None else "n/a",
            format_optional(status["log_age_seconds"], "s", 0),
            format_optional(status["cpu_percent"], "%"),
            format_optional(status["memory_mb"], "MB"),
            format_optional(status["gpu_percent"], "%", 0),
            detail,
        )

    healthy_count = sum(status["healthy"] for status in statuses.values())
    level = logging.INFO if healthy_count == len(MODELS) else logging.WARNING
    logging.log(
        level,
        "summary healthy=%d total=%d run_id=%s",
        healthy_count,
        len(MODELS),
        run_id,
    )
    return statuses


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor scaling-law vLLM workers")
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--interval", type=int, default=30)
    parser.add_argument("--stale-seconds", type=int, default=4000)
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path(__file__).with_name("monitor.log"),
    )
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    if args.interval <= 0:
        parser.error("--interval must be greater than zero")
    if args.stale_seconds <= 0:
        parser.error("--stale-seconds must be greater than zero")
    return args


def main():
    args = parse_args()
    configure_logging(args.log_file)
    logging.info(
        "starting monitor run_id=%s interval=%ss stale_after=%ss log_file=%s",
        args.run_id,
        args.interval,
        args.stale_seconds,
        args.log_file,
    )

    try:
        while True:
            check_all_models(args.run_id, args.stale_seconds)
            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logging.info("monitor stopped by user")


if __name__ == "__main__":
    main()
