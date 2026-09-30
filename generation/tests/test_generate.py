from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys
from unittest.mock import patch

import yaml

from generation.vllm import generate
from generation.vllm import launch_server


class GenerationPipelineTests(unittest.TestCase):
    def test_server_config_builds_expected_vllm_command(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "server.yaml"
            config_path.write_text(
                yaml.safe_dump(
                    {
                        "model": "generation/models/test-model",
                        "served_model_name": "test-model",
                        "host": "127.0.0.1",
                        "port": 9999,
                        "gpu": "3",
                        "enable_prefix_caching": True,
                        "disable_log_requests": False,
                    }
                ),
                encoding="utf-8",
            )

            with patch.object(
                sys,
                "argv",
                ["launch_server", "--config", str(config_path)],
            ), patch.object(launch_server.subprocess, "run") as run:
                launch_server.main()

            command = run.call_args.args[0]
            self.assertEqual(command[:3], ["vllm", "serve", "generation/models/test-model"])
            self.assertIn("--enable-prefix-caching", command)
            self.assertNotIn("--disable-log-requests", command)
            self.assertEqual(run.call_args.kwargs["cwd"], launch_server.ROOT_DIR)
            self.assertEqual(run.call_args.kwargs["env"]["CUDA_VISIBLE_DEVICES"], "3")
            self.assertTrue(run.call_args.kwargs["check"])

    def test_config_search_writes_manifest_config_and_jsonl(self) -> None:
        async def fake_run_inference(
            tasks,
            base_url,
            model_name,
            sampling_params,
            concurrency,
        ):
            self.assertEqual(base_url, "http://127.0.0.1:9999")
            self.assertEqual(model_name, "test-model")
            self.assertEqual(concurrency, 2)
            return [
                {
                    "task_id": task["task_id"],
                    "dataset": task["dataset"],
                    "prompt": "test prompt",
                    "prediction": "print(42)",
                    "finish_reason": "stop",
                    "usage": {"completion_tokens": 3},
                }
                for task in tasks
            ]

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tasks_path = root / "tiny_subset.jsonl"
            tasks_path.write_text(
                json.dumps(
                    {
                        "task_id": "tiny/1",
                        "dataset": "tiny",
                        "prompt": "Print 42.",
                        "prompt_type": "stdin_stdout",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            experiment_path = root / "experiment.yaml"
            experiment_path.write_text(
                yaml.safe_dump(
                    {
                        "protocol": "solve_at_1",
                        "batch_size": 1,
                        "concurrency": 2,
                        "task_paths": [str(tasks_path)],
                        "sampling_configs": {
                            "no_thinking_4k": {
                                "max_tokens": 4096,
                                "chat_template_kwargs": {
                                    "enable_thinking": False
                                },
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            runs_dir = root / "runs"
            with patch.object(generate, "DEFAULT_RUNS_DIR", runs_dir), patch.object(
                generate,
                "run_inference",
                new=fake_run_inference,
            ):
                generate.run_config_search(
                    experiment_path=experiment_path,
                    run_id="smoke",
                    model_name="test-model",
                    base_url="http://127.0.0.1:9999",
                )

            model_dir = runs_dir / "smoke" / "models" / "test-model"
            manifest = json.loads((model_dir / "manifest.json").read_text())
            self.assertEqual(manifest["run_id"], "smoke")
            self.assertEqual(manifest["model"], "test-model")

            config_dir = model_dir / "no_thinking_4k"
            self.assertTrue((config_dir / "config.json").is_file())
            result_path = config_dir / "tiny_generations.jsonl"
            rows = [json.loads(line) for line in result_path.read_text().splitlines()]
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["task_id"], "tiny/1")
            self.assertEqual(rows[0]["prediction"], "print(42)")
            self.assertEqual(rows[0]["config_name"], "no_thinking_4k")


if __name__ == "__main__":
    unittest.main()
