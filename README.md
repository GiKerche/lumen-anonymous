# Lumen-bench

A multilingual benchmark for evaluating what tool-calling language models **do**, not just what they say. It measures harmful tool use, including cases where a model refuses in words but still performs the requested action.

[Anonymous paper](release/lumen-bench.pdf) · [Dataset](data/) · [Reproduction guide](docs/reproduction.md)

This is the anonymous review artifact. In the anonymous repository viewer, use the **Website** button to open the interactive explorer. Both views use the same snapshot of `main`.

The benchmark evaluates **30 models** on **108 scenarios**, in Portuguese, English, Spanish, Mandarin Chinese, and Hindi, with six pressure conditions, two system prompts, and 21 tools: **194,400 trials**. It also includes 3,300 benign-control trials.

## Repository structure

| Location | Contents |
|---|---|
| `questions_v3_*.json`, `tool/`, `configs/` | Evaluation questions, tools, and model settings |
| `eval_results_consolidated/`, `eval_results_benign_control/` | Recorded model responses |
| `benign_control_questions/`, `benign_control_scored/` | The 11 benign tasks and completion scores for all 3,300 trials |
| `data/` | Parallel corpus, response records, human calibration, and judge labels |
| `analysis/revision/` | Analysis-ready records, statistics, benign controls, and sandbox results |
| `scripts/` | Data preparation and reproduction scripts |
| `release/` | Paper PDF, Overleaf ZIP, and arXiv source package |
| `site/`, `docs/` | Interactive explorer source and Pages copy: responses, judges, scenarios, and benign controls |

For analysis, start with [`corrected_records.csv.gz`](analysis/revision/corrected_records.csv.gz): it links each trial to its input, response, and judgment. It retains all 194,400 trials; 32 malformed tool-output errors are excluded from harmful-action rates, not counted as refusals.

## Reproduce the results

```bash
pip install -r requirements.txt
python scripts/analyze_revision.py --panel corrected --available-case --regression
```

If an anonymous host omits files above its size limit, run `python scripts/restore_large_files.py` first. The small files in [`artifact_parts/`](artifact_parts/) reconstruct the originals with SHA-256 verification; existing files are never overwritten. The interactive explorer already uses smaller data files.

This uses saved records, requires no API key, and makes no model API calls. See the [reproduction guide](docs/reproduction.md) for the full workflow, data fields, and paper compilation.

The [explorer guide](docs/explorer.md) explains local preview and GitHub Pages deployment.

All scenarios and tool effects are synthetic. Human calibration was conducted in Portuguese only; the benchmark does not establish safety in deployed agents.

## License and citation

Code: [MIT](LICENSE). Dataset: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Anonymous authors. *Lumen-bench: Cross-Lingual Safety Gaps and the Say-Do Problem in Tool-Calling Large Language Models.* 2026.
