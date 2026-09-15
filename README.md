<p align="center">
  <img src="./assets/banner.png" width="100%">
</p>

<h1 align="center">IR Lab</h1>

<p align="center">
  A from-scratch Information Retrieval framework: indexing, Boolean and TF-IDF retrieval,
  and research-grade evaluation -- built and tested against real IR test collections.
</p>

<p align="center">
  <a href="https://github.com/omarbounawarapy/IR-lab/actions/workflows/tests.yml"><img src="https://github.com/omarbounawarapy/IR-lab/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License: Apache 2.0"></a>
  <img src="https://img.shields.io/badge/python-3.12%2B-blue.svg" alt="Python 3.12+">
</p>

IR Lab is an educational and experimental Python package for building and studying
information retrieval systems from first principles. Rather than wrapping an existing
search library, it implements the pipeline itself -- analysis, indexing, retrieval, and
evaluation -- as small, independently testable components composed via declarative
configuration.

## Who this is for

Anyone who wants to understand *how* a search engine works by building one: students,
IR/ML engineers refreshing fundamentals, or contributors looking for a small, well-tested
codebase to extend with new retrieval models or metrics.

## Key features

- **Boolean retrieval** over a positional inverted index, with a real query-language
  pipeline (tokenizer &rarr; AST builder &rarr; RPN evaluator).
- **TF-IDF retrieval** as a second, structurally different retrieval model, enabling
  controlled model-vs-model comparisons on the same dataset.
- **Composable analysis pipeline**: character filters, tokenizers, and token filters,
  assembled from declarative JSON configuration -- no code changes needed to vary an
  experiment.
- **Research-grade evaluation**: precision/recall/F1, MAP, MRR, and nDCG@k, computed
  against real relevance judgments (qrels).
- **Paired significance testing** (paired t-test over per-topic Average Precision) for
  comparing two runs honestly, not just by point estimate.
- **Reproducible experiment runs**: every run persists its full config, code version, and
  per-query evaluation, so results can be reloaded and verified without re-running.
- **Real test collections**: ships with loaders/parsers for CISI (1460 docs, 112 queries)
  and Cranfield, plus a small toy dataset for fast iteration.

## Quick start

Requires Python 3.12+.

```bash
git clone https://github.com/omarbounawarapy/IR-lab.git
cd IR-lab
pip install -e ".[dev]"
pytest
```

## Usage examples

### 1. Run the bundled toy experiment (Boolean vs. TF-IDF, same dataset)

```bash
python3 -c "
import json
from ir_lab.core import ExpirimentRunner
from ir_lab.persistence.dataset.dataset_store import DatasetStore
from ir_lab.persistence.index.index_store import IndexStore

config = json.load(open('experiments/configs/toy_boolean_vs_tfidf.json'))
runner = ExpirimentRunner(DatasetStore(), IndexStore())
print(runner(config))
"
```

### 2. Fetch a real test collection

```bash
python3 scripts/download_cisi.py   # downloads + verifies CISI into datasets/cisi/
```

### 3. Reproduce the capstone experiment

A full hypothesis-driven research example -- does disabling punctuation filtering change
TF-IDF effectiveness (MAP) on CISI? -- with a controlled comparison and paired
significance test, entirely reproducible from persisted artifacts:

```bash
python3 scripts/run_capstone.py
```

See [`experiments/capstone/README.md`](experiments/capstone/README.md) for the full
write-up, methodology, and result (t = 1.542, df = 111, p = 0.126 -- not significant).

### 4. Reproduce the black-box case study (effectiveness + runtime + memory)

A black-box test of TF-IDF and Boolean retrieval on CISI, driven entirely through the
framework's public API and measuring runtime and peak memory per run, not just
effectiveness:

```bash
python3 scripts/run_case_study.py
```

See [`experiments/case_study/README.md`](experiments/case_study/README.md) for the full
methodology and results, including two findings surfaced by the test itself and fixed or
documented in place: an unhandled-input crash in Boolean retrieval (now fixed), and
TF-IDF's lack of a top-k cutoff.

### 5. Compare two runs programmatically

```python
from ir_lab.core.comparison import compare_runs

comparison = compare_runs(run_a_record, run_b_record, varying={"analysis"})
```

`compare_runs` raises a `ConfigError` if anything *other* than the declared `varying`
dimension differs between the two runs, so an experiment can't silently compare apples to
oranges.

## Project structure

```text
.
├── experiments/            # declarative experiment configs + capstone/case-study write-ups
├── scripts/                 # dataset download/parse scripts, capstone + case-study runners
├── src/ir_lab/
│   ├── analyzing/            # character filters, tokenizers, token filters, analyzers
│   ├── core/                 # experiment runner, component builder, run comparison
│   ├── evaluation/           # precision/recall/F1, MAP/MRR/nDCG, significance testing
│   ├── indexing/              # incidence matrix, inverted index, skip lists
│   ├── models/                 # documents, queries, datasets, qrels, experiments
│   ├── persistence/            # dataset/index/run stores and registries
│   └── processing/             # Boolean (AST/RPN) and TF-IDF retrieval pipelines
├── tests/                   # acceptance tests, one file per capability area
└── datasets/                # toy dataset (checked in); CISI/Cranfield fetched via scripts/
```

## Design philosophy

- Modularity over monolithic implementations -- every pipeline stage is independently
  testable.
- Experiments as configuration, not code: varying a dimension (dataset, analysis,
  retrieval model) should never require touching framework internals.
- Honesty over impressive-looking numbers: comparisons enforce controlled variables and
  are backed by significance tests, not just point estimates.

## Roadmap

- Additional ranking models (e.g. BM25)
- Expanded evaluation pipelines and benchmark comparisons
- More end-to-end example experiments

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).
Changes are tracked in [CHANGELOG.md](CHANGELOG.md). Found a security issue? See
[SECURITY.md](SECURITY.md).

## License

Apache License 2.0 -- see [LICENSE](LICENSE).
