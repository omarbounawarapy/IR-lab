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

### Boolean over CISI (`cisi_boolean.json`) -- fixed, now succeeds

Originally, running the framework's boolean retrieval model over CISI's
topic queries raised `IndexError: list index out of range` inside
`boolean_evaluator.py::evaluate_term`, before any results were produced.

**Root cause:** `BooleanEvaluator.evaluate_term` assumed every `TERM`
fragment analyzes to at least one token and read `tokens[0]` unconditionally.
A term made entirely of characters the analyzer discards (e.g. a lone `?`
or `...` left isolated by whitespace once punctuation filtering runs)
analyzes to zero tokens, so `tokens[0]` raised. 24 such empty-token
fragments occur across CISI's 112 queries.

**Fix (`boolean_evaluator.py`):** `evaluate_term` now returns `[]` -- no
matching documents -- when a term analyzes to zero tokens, the same
convention `InvertedIndex.get_postings` already uses for a term that
isn't in the vocabulary at all. No other file changed; `pytest` (42 tests)
still passes.

With that fixed, boolean retrieval now runs end to end on CISI:

| Effectiveness | Value |
|---|---|
| Precision | 0.0615 |
| Recall | 0.1183 |
| F1 | 0.0422 |
| MAP | 0.0153 |
| MRR | 0.1448 |
| nDCG@10 | 0.0637 |

| Performance | Value |
|---|---|
| Process wall time (`/usr/bin/time`, cold+warm+startup) | 1.48 s |
| Peak RSS | 131,828 KB (~129 MB) |
| Cold run (index build + retrieve, 112 queries) | 1.18 s |
| &nbsp;&nbsp;of which index build | 1.04 s |
| Warm run (retrieve only, 112 queries, index cached) | 0.14 s |
| Retrieved docs total / avg per query | 28,363 / ~253 |

**Caveat -- these numbers should not be read as "boolean retrieval on
CISI":** the RPN parser only recognizes the literal English words
`and`/`or`/`not` as operators; every other adjacent pair of terms in a
natural-language query is left unconnected. `ASTBuilder` builds an AST
per *connected* run of terms but never combines separate runs -- it just
leaves each one on its node stack, and `ASTTree.root()` returns only the
last one pushed. Concretely, for query 1 ("What problems and concerns are
there in making up descriptive titles? ...") the AST builder ends with 9
unconnected top-level nodes, and only the last -- `"descriptive" and
"titles"` -- is ever evaluated; the other 8 terms/subtrees are silently
dropped, no error or warning. So the boolean numbers above measure "AND of
whichever two terms happen to trail the last `and`/`or`/`not` in the
sentence" running successfully, not a faithful boolean interpretation of
the topic. That silent term-dropping is a distinct, still-open issue from
the crash fixed above (out of scope for this pass -- it's a query-language
semantics gap, not an unhandled-input crash) and is why the boolean
metrics differ so much from TF-IDF's despite the identical dataset,
analyzer and index.

## Findings

1. **TF-IDF has no top-k cutoff.** `TFIDFRetriever.score()` returns a score
   for every document sharing *any* query term with the query, and nothing
   truncates that list before it becomes the "retrieved" set. For a natural-
   language query with common terms, that is most of the 1,460-document
   collection (~1,441 of 1,460 per query here). This is why precision is
   ~0.02 despite recall of 0.67: precision/recall/F1 are only informative
   here for a ranked model once a cutoff (top-k) is introduced; MAP/MRR/
   nDCG@10 are the metrics that actually reflect ranking quality for this
   retrieval model as configured today.
2. **Boolean's query language silently drops unconnected terms** -- see the
   caveat above; not fixed in this pass.
3. **Cost profile:** for a 1,460-document, 112-query collection, both
   models fit comfortably under ~150 MB peak RSS and ~3 seconds of wall
   time single-threaded (import + dataset load + index build + retrieve +
   evaluate included), with index construction dominating -- roughly
   60-90% of that time -- and per-query retrieval on the order of single-
   digit milliseconds once the index exists.

## Files

- `cisi_tfidf.json`, `cisi_boolean.json` -- the experiment configs run.
- `cisi_tfidf.result.json`, `cisi_boolean.result.json` -- per-config worker
  output (timings + run-record summary, or the failure).
- `cisi_tfidf.time.log`, `cisi_boolean.time.log` -- raw `/usr/bin/time -v`
  output per config, regenerated on every run; not committed (matched by
  the repo's `*.log` gitignore rule).
- `runs/` -- the framework's own persisted run records (`RunStore`), one
  per config, exactly as `run_capstone.py` produces them; only the cold
  run is persisted (see worker script) to avoid a near-duplicate record
  for the warm timing pass.
- `results.json` -- the aggregated summary consumed above.
