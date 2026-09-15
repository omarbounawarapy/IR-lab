"""Reproducibility and persistence acceptance tests: the same config produces byte-identical
results twice, and a past run's exact config and result can be found
again from its run id alone -- no other context, no re-running anything.
"""
import json

from ir_lab.core import ExpirimentRunner
from ir_lab.persistence.dataset.dataset_store import DatasetStore
from ir_lab.persistence.index.index_store import IndexStore
from ir_lab.persistence.run.run_store import RunStore


def load_config():
    return json.load(open("experiments/configs/toy_inverted_index.json"))


def test_two_consecutive_runs_produce_identical_results():
    config = load_config()
    first = ExpirimentRunner(DatasetStore(), IndexStore())(config)
    second = ExpirimentRunner(DatasetStore(), IndexStore())(config)

    first_ids = [[doc.id for doc in r] for r in first["example"]]
    second_ids = [[doc.id for doc in r] for r in second["example"]]
    assert first_ids == second_ids


def test_run_is_persisted_and_retrievable_by_id_alone(tmp_path):
    run_store = RunStore(root=str(tmp_path))
    runner = ExpirimentRunner(DatasetStore(), IndexStore(), run_store=run_store)
    runner(load_config())

    run_ids = run_store.list()
    assert len(run_ids) == 1

    record = run_store.load(run_ids[0])
    # The config and the result live in the same record -- structurally
    # linked, not filename-adjacent.
    assert record["run_config_id"] == "example"
    assert record["config"]["retrieval"]["type"] == "boolean"
    assert record["dataset_id"] == "toy"
    assert record["retrieved"][0] == [1, 5]
    assert record["retrieved"][1] == [2, 3]
    assert record["retrieved"][2] == []
    assert record["code_version"]
    assert record["created_at"]


def test_persisted_run_carries_its_own_evaluation(tmp_path):
    run_store = RunStore(root=str(tmp_path))
    runner = ExpirimentRunner(DatasetStore(), IndexStore(), run_store=run_store)
    runner(load_config())

    record = run_store.load(run_store.list()[0])
    assert record["evaluation"][0] == {"query_id": 1, "precision": 0.5, "recall": 1.0, "f1": 2 / 3}


def test_missing_run_id_is_a_legible_data_error(tmp_path):
    from ir_lab.errors import DataError
    import pytest

    run_store = RunStore(root=str(tmp_path))
    with pytest.raises(DataError):
        run_store.load("does-not-exist")


def test_two_runs_of_the_same_config_get_distinct_run_ids(tmp_path):
    run_store = RunStore(root=str(tmp_path))
    runner = ExpirimentRunner(DatasetStore(), IndexStore(), run_store=run_store)
    config = load_config()
    runner(config)
    runner(config)

    assert len(run_store.list()) == 2
