# Stage 5: Correctness test harness

The harness streams benchmark records and the 20 matching model/configuration
generation files in lockstep. Each yielded task contains its tests and all 20
normalized predictions. A bounded `ProcessPoolExecutor` evaluates several
tasks concurrently without loading the complete run into memory.

Every candidate program is written to a temporary directory and executed with
the isolated judge interpreter. Test input is supplied on stdin, stdout is
compared after trimming outer whitespace, and timeouts or runtime failures are
recorded as structured CSV rows.

## Judge environment

```bash
python3 -m venv test_harness/.venv
test_harness/.venv/bin/python -m pip install \
  -r test_harness/requirements.txt
```

## Smoke test

```bash
test_harness/.venv/bin/python -m test_harness.harness \
  --workers 1 \
  --max-in-flight 1 \
  --limit 1 \
  --output /tmp/compression_law_smoke.csv \
  --overwrite
```

## Full run

```bash
test_harness/.venv/bin/python -m test_harness.harness \
  --workers 4 \
  --max-in-flight 8 \
  --output analysis/outputs/correctness_results.csv \
  --overwrite
```

The current judge covers stdin/stdout APPS and LiveCodeBench programs. The 98
APPS function-call tasks reported as unsupported require a separate evaluator.
