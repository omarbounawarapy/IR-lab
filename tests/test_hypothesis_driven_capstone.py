"""Hypothesis-driven capstone acceptance test: the capstone's persisted artifacts alone
-- no re-running the experiment -- are enough for a reviewer to verify
every step: the two configs differ only in the declared variable, the
persisted runs' evaluation matches what's reported, and the checked-in
comparison.json is exactly what compare_runs produces from those runs.
"""
import json
from pathlib import Path

from ir_lab.core.comparison import compare_runs
from ir_lab.persistence.run.run_store import RunStore

CAPSTONE_DIR = Path("experiments/capstone")


def load_capstone_configs():
    with_filter = json.load(open(CAPSTONE_DIR / "cisi_tfidf_with_punctuation_filter.json"))
    without_filter = json.load(open(CAPSTONE_DIR / "cisi_tfidf_without_punctuation_filter.json"))
    return with_filter, without_filter


def test_the_two_configs_differ_only_in_the_declared_variable():
    with_filter, without_filter = load_capstone_configs()

    run_a = with_filter["runs"][0]
    run_b = without_filter["runs"][0]

    assert with_filter["dataset"] == without_filter["dataset"]
    assert run_a["retrieval"] == run_b["retrieval"]
    assert run_a["index"] == run_b["index"]
    assert run_a["analysis"] != run_b["analysis"]  # the one declared variable


def test_persisted_runs_exist_and_are_loadable_without_rerunning():
    run_store = RunStore(root=str(CAPSTONE_DIR / "runs"))
    run_ids = run_store.list()
    assert len(run_ids) == 2

    records = {run_store.load(rid)["run_config_id"]: run_store.load(rid) for rid in run_ids}
    assert set(records) == {"with_punctuation_filter", "without_punctuation_filter"}

    for record in records.values():
        assert record["dataset_id"] == "cisi"
        assert len(record["queries"]) == 112
        assert record["evaluation"] is not None
        assert record["ranked_evaluation"] is not None
        assert record["code_version"]


def test_checked_in_comparison_is_exactly_reproducible_from_persisted_runs():
    run_store = RunStore(root=str(CAPSTONE_DIR / "runs"))
    records = {run_store.load(rid)["run_config_id"]: run_store.load(rid) for rid in run_store.list()}

    recomputed = compare_runs(
        records["with_punctuation_filter"],
        records["without_punctuation_filter"],
        varying={"analysis"},
    )

    checked_in = json.load(open(CAPSTONE_DIR / "comparison.json"))

    # run ids are freshly generated per execution and aren't part of the
    # scientific claim; everything else must match exactly.
    for key in ("varying", "metrics_a", "metrics_b", "ranked_metrics_a", "ranked_metrics_b", "significance"):
        assert recomputed[key] == checked_in[key]


def test_conclusion_is_backed_by_a_real_non_significant_p_value():
    comparison = json.load(open(CAPSTONE_DIR / "comparison.json"))
    # The written conclusion claims the MAP difference is not
    # significant at the conventional threshold -- verify the number
    # backing that claim is actually what's checked in, not asserted.
    assert comparison["significance"]["p_value"] > 0.05
    assert comparison["significance"]["n_topics"] == 112
