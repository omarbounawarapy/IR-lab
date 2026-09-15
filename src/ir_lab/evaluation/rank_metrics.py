"""Rank-aware effectiveness measures: AP/MAP, RR/MRR, nDCG@k.

Built on top of the same relevant_documents() binary-relevance judgment
as the L5 precision/recall/F1 core (evaluation/metrics.py). Tie-breaking
convention for nDCG's ideal ranking is documented explicitly at the
function it applies to, per the failure mode the assessment named:
"nDCG computed without a defined tie-breaking convention."
"""
import math


def average_precision(retrieved: list, relevant: set) -> float:
    if not relevant:
        return 0.0
    relevant = set(relevant)
    hits = 0
    precisions = []
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            hits += 1
            precisions.append(hits / rank)
    if not precisions:
        return 0.0
    return sum(precisions) / len(relevant)


def reciprocal_rank(retrieved: list, relevant: set) -> float:
    relevant = set(relevant)
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0


def dcg_at_k(retrieved: list, relevant: set, k: int) -> float:
    relevant = set(relevant)
    return sum(
        1.0 / math.log2(rank + 1)
        for rank, doc_id in enumerate(retrieved[:k], start=1)
        if doc_id in relevant
    )


def ndcg_at_k(retrieved: list, relevant: set, k: int) -> float:
    """With binary relevance, the ideal ranking is any ordering of the
    relevant documents first -- ideal DCG@k only depends on how many of
    them fit within the first k ranks, not on their order, so this
    doesn't need to pick a tie-breaking order among equally-relevant
    documents."""
    ideal = dcg_at_k(list(relevant), relevant, k)
    if ideal == 0.0:
        return 0.0
    return dcg_at_k(retrieved, relevant, k) / ideal


def evaluate_ranked_query(retrieved: list, relevant: set, k: int = 10) -> dict:
    return {
        "ap": average_precision(retrieved, relevant),
        "rr": reciprocal_rank(retrieved, relevant),
        f"ndcg@{k}": ndcg_at_k(retrieved, relevant, k),
    }


def evaluate_ranked_run(queries, run_results, qrels, k: int = 10) -> list[dict]:
    from .metrics import relevant_documents

    per_query = []
    for query, scored_docs in zip(queries, run_results):
        retrieved = [doc.id for doc in scored_docs]
        relevant = relevant_documents(qrels, query.id)
        per_query.append({
            "query_id": query.id,
            **evaluate_ranked_query(retrieved, relevant, k),
        })
    return per_query


def mean_average_precision(per_query: list[dict]) -> float:
    return sum(q["ap"] for q in per_query) / len(per_query)


def mean_reciprocal_rank(per_query: list[dict]) -> float:
    return sum(q["rr"] for q in per_query) / len(per_query)


def mean_ndcg(per_query: list[dict], k: int = 10) -> float:
    key = f"ndcg@{k}"
    return sum(q[key] for q in per_query) / len(per_query)
