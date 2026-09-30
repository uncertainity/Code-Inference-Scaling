# Stage 1: Data collection and cleaning

This stage downloads the source benchmarks, converts them to one common JSONL
schema, locates missing or unparsable reference programs, and incorporates
replacement solutions. The Codex-authored APPS and LiveCodeBench solutions are
kept in `reference_solutions/codex/`.

## Layout

- `raw/`: downloaded Hugging Face datasets (local artifact, not committed)
- `normalized/`: common-schema JSONL (local artifact, not committed)
- `reference_solutions/codex/`: generated replacements for missing solutions
- `reference_solutions/scraped/`: solutions collected from source platforms
- `reference_solutions/vendor/`: external solution repositories
- `reference_solutions/missing/`: tasks needing a replacement solution
- `metadata/`: platform lookup information
- `prompts/`: instructions used to create missing reference solutions
- `scripts/`: collection, inspection, normalization, and merge utilities

## Typical workflow

```bash
# Download MBPP, HumanEval, APPS, and LiveCodeBench.
python -m data_collection.scripts.download_datasets

# Inspect a downloaded dataset.
python -m data_collection.scripts.inspect_datasets \
  --dataset apps --split test -n 3

# After schema/trace extraction, list tasks without usable reference code.
python -m data_collection.scripts.filter_missing_solutions

# Normalize generated replacement files and then merge them into the data.
python -m data_collection.scripts.normalize_codex_solutions
python -m data_collection.scripts.merge_codex_solutions

# Refresh dataset counts and integrity summaries.
python -m data_collection.scripts.data_statistics
```

The APPS replacements use `complexity_metrics.dataset_schema`; the LCB
replacements use the platform-aware logic in `complexity_metrics.lcb_schema`.
See [`prompts/codex_prompt.md`](prompts/codex_prompt.md) for the replacement-code
contract.

The scripts do not silently download or rewrite data when imported; work only
starts through their command-line entry points.

