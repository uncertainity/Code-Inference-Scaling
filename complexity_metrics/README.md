# Stage 3: Complexity metrics

This stage normalizes source records and measures the reference programs used
to stratify benchmark difficulty.

The trace schema includes:

- AST node counts and structural features;
- cyclomatic complexity;
- Halstead metrics;
- raw source metrics; and
- maintainability index.

## Components

- `ast_metrics.py`: shared AST and Radon metric implementation
- `dataset_schema.py`: MBPP, HumanEval, and APPS normalization/trace extraction
- `lcb_schema.py`: LiveCodeBench normalization and reference-code recovery
- `traces/`: full pre-fair task traces
- `fair_traces/`: traces aligned with `fair_data/data_jsonl/`
- `plot_metric_averages.py`: dataset-level metric comparison

To regenerate the dataset-level plot after the aligned traces exist:

```bash
python complexity_metrics/plot_metric_averages.py
```

The checked-in trace files are the exact complexity inputs consumed by the
complexity-conditioned correctness analysis.

