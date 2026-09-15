"""Basic effectiveness measurement: precision, recall, F1 against qrels.

Rank-aware measures (MAP, MRR, nDCG) and significance testing are a later,
separate module -- this module only covers the unranked precision/recall/F1
core, including the two edge cases that are easy to get wrong: an empty
result set, and a query with zero relevant documents in the qrels.
"""
from ir_lab.models.relevance import Qrel


def relevant_documents(qrels: list[Qrel], query_id, threshold: int = 1) -> set:
    """The set of document ids judged relevant (relevance >= threshold)
    for a given query, from a flat list of Qrel judgments.

    A judgment with no explicit "relevance" field (e.g. CISI's qrels,
    which only record query/document pairs) is treated as relevant --
    for collections like that, appearing in the qrels at all *is* the
    judgment. A judgment that does carry a relevance field is scored
    against it, so an explicit 0 is still correctly excluded.
    """
    return {
        qrel.document_id
        for qrel in qrels
        if qrel.query_id == query_id
        and (qrel.metadata or {}).get("relevance", 1) >= threshold
    }


def precision(retrieved: list, relevant: set) -> float:
    """Fraction of retrieved documents that are relevant.

    An empty result set has precision 0.0 by convention (there is nothing
    to divide by len(retrieved), so this is defined, not computed).
    """
    if not retrieved:
        return 0.0
    relevant = set(relevant)
    hits = sum(1 for doc_id in retrieved if doc_id in relevant)
    return hits / len(retrieved)


def recall(retrieved: list, relevant: set) -> float:
    """Fraction of relevant documents that were retrieved.

    A query with zero relevant documents in the qrels has recall 0.0 by
    convention -- there is nothing to divide by len(relevant), so this
    avoids a ZeroDivisionError rather than silently mis-scoring the query.
    """
    if not relevant:
        return 0.0
    relevant = set(relevant)
    hits = sum(1 for doc_id in retrieved if doc_id in relevant)
    return hits / len(relevant)


def f1(precision_value: float, recall_value: float) -> float:
    """Harmonic mean of precision and recall; 0.0 when both are 0."""
    if precision_value + recall_value == 0:
        return 0.0
    return 2 * precision_value * recall_value / (precision_value + recall_value)


METRICS = {
    "precision": lambda retrieved, relevant: precision(retrieved, relevant),
    "recall": lambda retrieved, relevant: recall(retrieved, relevant),
    "f1": lambda retrieved, relevant: f1(precision(retrieved, relevant), recall(retrieved, relevant)),
}


def evaluate_query(retrieved: list, relevant: set, metric_names=("precision", "recall", "f1")) -> dict:
    return {name: METRICS[name](retrieved, relevant) for name in metric_names}


def evaluate_run(queries, run_results, qrels, metric_names=("precision", "recall", "f1")) -> list[dict]:
    """Score a completed run's per-query results against qrels.

    `run_results` is the list-of-ScoredDocument-lists a processor returns
    for `queries`, in the same order. This is the connection point a
    completed run's output is scored through, with no per-experiment glue
    code required.
    """
    per_query = []
    for query, scored_docs in zip(queries, run_results):
        retrieved = [doc.id for doc in scored_docs]
        relevant = relevant_documents(qrels, query.id)
        per_query.append({
            "query_id": query.id,
            **evaluate_query(retrieved, relevant, metric_names),
        })
    return per_query
