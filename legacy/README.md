# Legacy archive

This directory preserves superseded material for provenance. It is not imported
or called by the supported six-stage pipeline.

- `prototypes/`: rough schema, metric, loading, and serving experiments
- `judges/`: correctness harnesses replaced by `test_harness/`
- `generation/`: dummy serving code and obsolete vLLM configs
- `runs/`: older generation searches
- `fair_data_experiments/`: pre-scaling-law result layouts
- `monitoring/`: old heartbeat tooling and logs
- `python_packages/`: abandoned package shells
- `notes/`: historical notes
- `cache/`: Python bytecode moved out of the active tree

Large historical outputs and caches remain available in the working directory
but are excluded from Git. New work should not add dependencies on this tree.

