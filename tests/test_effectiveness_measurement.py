"""Effectiveness-measurement acceptance tests: precision/recall/F1, computed against the real
toy dataset's qrels and the happy-path suite's known-correct query results, match
hand-calculated values exactly -- including the empty-result and
zero-relevant-documents edge cases.
"""
import pytest

from ir_lab.evaluation.metrics import (
    evaluate_query,
    evaluate_run,
    f1,
    precision,
    recall,
    relevant_documents,
)
from ir_lab.models.queries import Query
from ir_lab.models.documents import ScoredDocument
from ir_lab.persistence.dataset.dataset_store import DatasetStore


@pytest.fixture(scope="module")
def toy_dataset():
    return DatasetStore().load("toy")


def test_relevant_documents_reads_binary_threshold_from_qrels(toy_dataset):
    # query 1's qrels: doc 1 relevant (x2, duplicated in the source file),
    # doc 4 explicitly judged non-relevant.
    assert relevant_documents(toy_dataset.qrels, 1) == {1}
    assert relevant_documents(toy_dataset.qrels, 2) == {2, 3}
    assert relevant_documents(toy_dataset.qrels, 3) == {2, 4}


def test_precision_recall_f1_against_hand_computed_values(toy_dataset):
    # These are exactly the happy-path suite's boolean-retrieval results for the toy
    # dataset's three real queries (tests/test_legible_failure_and_config.py: "index and
    # posting" -> [1, 5], "boolean or vector" -> [2, 3], "retrieval and
    # vector" -> []).
    cases = [
        (1, [1, 5], {"precision": 0.5, "recall": 1.0, "f1": 2 / 3}),
        (2, [2, 3], {"precision": 1.0, "recall": 1.0, "f1": 1.0}),
        (3, [], {"precision": 0.0, "recall": 0.0, "f1": 0.0}),
    ]
    for query_id, retrieved, expected in cases:
        relevant = relevant_documents(toy_dataset.qrels, query_id)
        scores = evaluate_query(retrieved, relevant)
        assert scores["precision"] == pytest.approx(expected["precision"])
        assert scores["recall"] == pytest.approx(expected["recall"])
        assert scores["f1"] == pytest.approx(expected["f1"])


def test_empty_result_set_is_a_defined_zero_not_a_crash():
    assert precision([], {1, 2, 3}) == 0.0
    assert recall([], {1, 2, 3}) == 0.0
    assert f1(0.0, 0.0) == 0.0


def test_zero_relevant_documents_is_a_defined_zero_not_a_crash():
    # A query with no relevant documents in the qrels is not hypothetical:
    # recall's denominator would otherwise be a ZeroDivisionError.
    assert recall([1, 2], set()) == 0.0
    assert precision([1, 2], set()) == 0.0


def test_evaluate_run_scores_a_full_processor_output(toy_dataset):
    queries = [Query(id=1, content="index and posting"), Query(id=2, content="boolean or vector")]
    run_results = [
        [ScoredDocument(1), ScoredDocument(5)],
        [ScoredDocument(2), ScoredDocument(3)],
    ]
    scored = evaluate_run(queries, run_results, toy_dataset.qrels)
    assert scored[0] == {"query_id": 1, "precision": 0.5, "recall": 1.0, "f1": pytest.approx(2 / 3)}
    assert scored[1] == {"query_id": 2, "precision": 1.0, "recall": 1.0, "f1": 1.0}
