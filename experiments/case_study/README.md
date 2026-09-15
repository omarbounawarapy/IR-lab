# Case study: black-box test of ir_lab on CISI

This is a black-box test of the framework as a *user* of it would run it --
only through `ExpirimentRunner`, `DatasetStore`, `IndexStore` and `RunStore`
(the same public surface `scripts/run_capstone.py` uses), never by importing
or exercising any internal module directly. Goal: capture effectiveness
*and* runtime/memory on a real dataset as a reusable reference point.

## Method

- **Dataset:** CISI -- 1,460 documents, 112 topic queries, 3,114 relevance
  judgments (`datasets/cisi`).
- **Systems under test:** the two retrieval models the framework currently
  registers in `ProcessorBuilder` -- `tfidf` and `boolean` -- both over an
  `inverted` index with the same analyzer (punctuation stripped, lowercased,
  space-tokenized).
- **Driver:** `scripts/run_case_study.py` shells out to
  `scripts/case_study_worker.py`, one fresh subprocess per config, wrapped
  in `/usr/bin/time -v`. Each config runs twice inside its subprocess:
  - **cold** -- index does not exist yet, so this is index-build +
    retrieval, timed with `time.perf_counter` around the whole
    `runner(config)` call.
  - **warm** -- same `ExpirimentRunner`/`IndexStore` instance, so the
    in-memory index from the cold run is reused; isolates retrieval-only
    latency.
- **Why a fresh subprocess per config:** `/usr/bin/time -v`'s "Maximum
  resident set size" is the peak for that one process. Measuring multiple
  configs in one long-lived process would only ever report a running
  maximum across them, not each config's own footprint.
- **Effectiveness:** precision/recall/F1 (unranked, `evaluation/metrics.py`)
  and MAP/MRR/nDCG@10 (ranked, `evaluation/rank_metrics.py`), both computed
  by the framework itself as part of `runner(config)` and persisted into
  `runs/` by `RunStore` -- not recomputed by this case study's own code.

Reproduce with:

```
python3 scripts/run_case_study.py
```

## Results

### TF-IDF over CISI (`cisi_tfidf.json`) -- succeeded

| Effectiveness | Value |
|---|---|
| Precision | 0.0198 |
| Recall | 0.6701 |
| F1 | 0.0374 |
| MAP | 0.0819 |
| MRR | 0.2613 |
| nDCG@10 | 0.1533 |

| Performance | Value |
|---|---|
| Process wall time (`/usr/bin/time`, cold+warm+startup) | 3.04 s |
| Peak RSS | 152,632 KB (~149 MB) |
| Cold run (index build + retrieve, 112 queries) | 2.04 s |
| &nbsp;&nbsp;of which index build | 1.22 s |
| Warm run (retrieve only, 112 queries, index cached) | 0.82 s |
| Retrieved docs total / avg per query | 161,484 / ~1,441 |

These effectiveness numbers match `experiments/capstone/comparison.json`'s
`metrics_a`/`ranked_metrics_a` exactly, which is an independent
cross-check: two different driver scripts, calling the framework the same
black-box way, reproduce identical numbers on the same config.

### Boolean over CISI (`cisi_boolean.json`) -- crashed

Running the framework's boolean retrieval model over CISI's topic queries
raises `IndexError: list index out of range` inside
`boolean_evaluator.py::evaluate_term`, before any results are produced.
Full traceback in `cisi_boolean.result.json`.

## Findings

1. **Boolean retrieval cannot run against CISI's queries.** CISI topics are
   natural-language questions ("What problems and concerns are there in
   making up descriptive titles?"), not boolean expressions. The RPN
   parser accepts a run of unconnected `TERM` tokens, but
   `BooleanAstBuilder`/`BooleanEvaluator` require every term to be joined by
   an explicit `and`/`or`/`not` -- a multi-term run with no connecting
   operator crashes rather than raising a `ConfigError` about the
   malformed query. Boolean retrieval is currently only exercisable with
   hand-written boolean-syntax queries, not off-the-shelf IR test
   collections.
2. **TF-IDF has no top-k cutoff.** `TFIDFRetriever.score()` returns a score
   for every document sharing *any* query term with the query, and nothing
   truncates that list before it becomes the "retrieved" set. For a natural-
   language query with common terms, that is most of the 1,460-document
   collection (~1,441 of 1,460 per query here). This is why precision is
   ~0.02 despite recall of 0.67: precision/recall/F1 are only informative
   here for a ranked model once a cutoff (top-k) is introduced; MAP/MRR/
   nDCG@10 are the metrics that actually reflect ranking quality for this
   retrieval model as configured today.
3. **Cost profile:** for a 1,460-document, 112-query collection, the whole
   pipeline (import + dataset load + index build + retrieve + evaluate)
   fits in ~150 MB peak RSS and ~2 seconds of wall time single-threaded, of
   which roughly 60% is index construction and 40% is retrieval across all
   112 queries -- i.e. per-query retrieval is on the order of a few
   milliseconds once the index exists.

## Files

- `cisi_tfidf.json`, `cisi_boolean.json` -- the experiment configs run.
- `cisi_tfidf.result.json`, `cisi_boolean.result.json` -- per-config worker
  output (timings + run-record summary, or the failure).
- `cisi_tfidf.time.log`, `cisi_boolean.time.log` -- raw `/usr/bin/time -v`
  output per config, regenerated on every run; not committed (matched by
  the repo's `*.log` gitignore rule).
- `runs/` -- the framework's own persisted run record(s) (`RunStore`),
  exactly as `run_capstone.py` produces them; only the cold run is
  persisted (see worker script) to avoid a near-duplicate record for the
  warm timing pass.
- `results.json` -- the aggregated summary consumed above.
