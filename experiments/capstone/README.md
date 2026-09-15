# Capstone: does punctuation filtering matter for TF-IDF on CISI?

**Research question.** Does disabling punctuation filtering change TF-IDF
retrieval effectiveness (MAP) on the CISI collection?

This is the capstone worked example: a one-sentence question, answered
by two configs differing in exactly one declared dimension, run through
the framework's own code with zero framework changes, compared under an
enforced controlled-comparison check, and backed by a paired significance
test -- with every number below independently reproducible from the
persisted artifacts in this directory alone.

## Why TF-IDF, and why not boolean, and why not the toy dataset

Two things were confirmed by actually running them, not assumed:

- CISI's queries are real natural-language questions ("What problems and
  concerns are there in making up descriptive titles?..."), not boolean
  expressions. Running them through the boolean query processor crashes,
  because words like "and"/"or"/"not" inside ordinary English sentences
  get parsed as boolean operators, producing malformed expressions the
  AST builder can't evaluate. This is a real, current architectural limit
  worth stating plainly rather than working around: boolean retrieval, as
  built, expects a query *language*, and CISI's queries were never written
  in one. TF-IDF's free-text scoring has no such requirement (it never
  parses the query as anything but a bag of words), so it runs on CISI
  cleanly -- this is exactly the point made earlier about the boolean-specific
  query-language pipeline vs. TF-IDF's genuinely different shape.
- The toy dataset (6 documents, 3 queries) is too small for a significance
  test to mean anything -- Section 3 of the assessment calls this out
  explicitly. CISI's 112 real queries and 1460 real documents are what
  make the significance test below meaningful rather than decorative.

## The two runs

- [`cisi_tfidf_with_punctuation_filter.json`](cisi_tfidf_with_punctuation_filter.json)
- [`cisi_tfidf_without_punctuation_filter.json`](cisi_tfidf_without_punctuation_filter.json)

Both: CISI dataset, inverted index, TF-IDF retrieval, space tokenizer,
lowercase token filter. The *only* declared difference is
`analysis.character_filters`: punctuation filtering on vs. off.

Reproduce with:

```
python3 scripts/run_capstone.py
```

This persists both runs (each with its embedded config, code version,
seed, and per-query evaluation) into [`runs/`](runs/) via `RunStore`, runs
them through `compare_runs(..., varying={"analysis"})` -- which would
raise `ConfigError` if anything *other* than `analysis` also differed
between the two configs -- and writes the result to
[`comparison.json`](comparison.json).

## Result

| | with punctuation filter | without punctuation filter |
|---|---:|---:|
| MAP | 0.0819 | 0.0734 |
| MRR | 0.2613 | 0.2376 |
| nDCG@10 | 0.1533 | 0.1289 |

Paired t-test on per-topic Average Precision across all 112 queries:
**t = 1.542, df = 111, p = 0.126**.

## Conclusion

Punctuation filtering is associated with a higher point-estimate MAP on
CISI (0.082 vs. 0.073), but the paired t-test over all 112 topics does
not reach significance at the conventional p < 0.05 threshold (p = 0.126).
The honest conclusion is **not** "punctuation filtering helps" -- it is
that this experiment, at this topic count, cannot distinguish the
observed difference from noise. That is not a disappointing result; it is
the exact failure mode Section 0.3 exists to prevent: a
plausible-looking effectiveness gap asserted as a real finding without
checking whether the topic set is large enough to support the claim.
A larger effect, a different variable, or a one-tailed hypothesis
motivated in advance could change this -- but that would be a new
experiment, not a reinterpretation of this one's p-value.
