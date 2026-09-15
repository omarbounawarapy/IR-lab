"""Research-grade evaluation acceptance tests: MAP/MRR/nDCG match hand-computed values, the
paired t-test matches an independent (scipy) reference to floating-point
tolerance, and a boolean-vs-tfidf comparison over a multi-query topic set
comes with a significance test attached.
"""
import json
import math

import pytest

from ir_lab.core import ExpirimentRunner
from ir_lab.core.comparison import compare_runs
from ir_lab.evaluation.rank_metrics import (
    average_precision,
    evaluate_ranked_run,
    mean_average_precision,
    mean_ndcg,
    mean_reciprocal_rank,
    ndcg_at_k,
    reciprocal_rank,
)
from ir_lab.evaluation.significance import paired_t_test
from ir_lab.models.queries import Query
from ir_lab.models.documents import ScoredDocument
from ir_lab.persistence.dataset.dataset_store import DatasetStore
from ir_lab.persistence.index.index_store import IndexStore
from ir_lab.persistence.run.run_store import RunStore


@pytest.fixture(scope="module")
def toy_dataset():
    return DatasetStore().load("toy")


def test_map_mrr_ndcg_against_hand_computed_values(toy_dataset):
    # the happy-path suite's known-correct boolean results for the toy dataset's three
    # real queries: [1, 5], [2, 3], [].
    queries = [Query(id=1, content=""), Query(id=2, content=""), Query(id=3, content="")]
    run_results = [
        [ScoredDocument(1), ScoredDocument(5)],
        [ScoredDocument(2), ScoredDocument(3)],
        [],
    ]
    per_query = evaluate_ranked_run(queries, run_results, toy_dataset.qrels, k=2)

    assert per_query[0]["ap"] == pytest.approx(1.0)
    assert per_query[0]["rr"] == pytest.approx(1.0)
    assert per_query[0]["ndcg@2"] == pytest.approx(1.0)

    assert per_query[1]["ap"] == pytest.approx(1.0)
    assert per_query[1]["rr"] == pytest.approx(1.0)
    assert per_query[1]["ndcg@2"] == pytest.approx(1.0)

    assert per_query[2]["ap"] == pytest.approx(0.0)
    assert per_query[2]["rr"] == pytest.approx(0.0)
    assert per_query[2]["ndcg@2"] == pytest.approx(0.0)

    assert mean_average_precision(per_query) == pytest.approx(2 / 3)
    assert mean_reciprocal_rank(per_query) == pytest.approx(2 / 3)
    assert mean_ndcg(per_query, k=2) == pytest.approx(2 / 3)


def test_average_precision_with_a_partial_hit():
    # retrieved = [A(miss), B(hit), C(miss), D(hit)], 2 relevant total.
    retrieved = ["A", "B", "C", "D"]
    relevant = {"B", "D"}
    # precision@2 = 1/2, precision@4 = 2/4 -> AP = (0.5 + 0.5) / 2 = 0.5
    assert average_precision(retrieved, relevant) == pytest.approx(0.5)
    assert reciprocal_rank(retrieved, relevant) == pytest.approx(0.5)


def test_ndcg_ideal_ranking_scores_one():
    retrieved = ["A", "B", "C"]
    relevant = {"A", "B"}
    assert ndcg_at_k(retrieved, relevant, k=3) == pytest.approx(1.0)


def test_paired_t_test_matches_independent_scipy_reference():
    # Cross-validated against scipy.stats.ttest_rel(a, b) at authoring
    # time (see the module docstring in significance.py for the method);
    # the exact float is hardcoded here so this test needs no scipy
    # dependency to run.
    a = [0.8, 0.6, 0.9, 0.7, 0.5, 0.85]
    b = [0.6, 0.55, 0.7, 0.65, 0.4, 0.6]
    result = paired_t_test(a, b)
    assert result["t_statistic"] == pytest.approx(4.029386436689804)
    assert result["p_value"] == pytest.approx(0.010027273612010142, rel=1e-9)
    assert result["degrees_of_freedom"] == 5


def test_paired_t_test_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        paired_t_test([1.0, 2.0], [1.0])


def test_paired_t_test_zero_variance_nonzero_mean_is_infinite_t_zero_p():
    result = paired_t_test([1.0, 1.0, 1.0], [0.5, 0.5, 0.5])
    assert math.isinf(result["t_statistic"])
    assert result["p_value"] == 0.0


def test_boolean_vs_tfidf_comparison_carries_a_significance_test(tmp_path):
    run_store = RunStore(root=str(tmp_path))
    runner = ExpirimentRunner(DatasetStore(), IndexStore(), run_store=run_store)
    config = json.load(open("experiments/configs/toy_boolean_vs_tfidf.json"))
    runner(config)

    records = {run_store.load(rid)["run_config_id"]: run_store.load(rid) for rid in run_store.list()}
    comparison = compare_runs(records["boolean_run"], records["tfidf_run"], varying={"retrieval"})

    assert comparison["ranked_metrics_a"] is not None
    assert comparison["ranked_metrics_b"] is not None
    assert comparison["significance"] is not None
    assert 0.0 <= comparison["significance"]["p_value"] <= 1.0
    assert comparison["significance"]["n_topics"] == 3
