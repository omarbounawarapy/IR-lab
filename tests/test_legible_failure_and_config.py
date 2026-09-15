"""Config-driven execution acceptance tests: an experiment is defined and run purely from a
config file, and every failure category (config / data / unsupported
feature) is attributable from the error message alone.
"""
import copy
import json

import pytest

from ir_lab.core import ExpirimentRunner
from ir_lab.errors import ConfigError, DataError, UnsupportedFeatureError
from ir_lab.persistence.dataset.dataset_store import DatasetStore
from ir_lab.persistence.index.index_store import IndexStore


def load_config(path="experiments/configs/toy_inverted_index.json"):
    return json.load(open(path))


def new_runner():
    return ExpirimentRunner(DatasetStore(), IndexStore())


def test_shipped_config_runs_unmodified_to_a_real_result():
    results = new_runner()(load_config())
    example = results["example"]
    assert [doc.id for doc in example[0]] == [1, 5]
    assert [doc.id for doc in example[1]] == [2, 3]
    assert [doc.id for doc in example[2]] == []


def test_a_second_config_varying_one_parameter_also_runs():
    # Proves execution isn't hardcoded to the one shipped example: disabling
    # the punctuation filter changes tokenization and therefore the result.
    results = new_runner()(load_config("experiments/configs/toy_boolean_no_punctuation_filter.json"))
    no_punct = results["no_punctuation"]
    assert [doc.id for doc in no_punct[0]] == [1]  # "index." != "index" now


def test_unknown_dataset_is_a_config_error():
    config = load_config()
    config["dataset"]["id"] = "does_not_exist"
    with pytest.raises(ConfigError):
        new_runner()(config)


def test_missing_dataset_field_is_a_config_error():
    config = load_config()
    del config["dataset"]["id"]
    with pytest.raises(ConfigError):
        new_runner()(config)


def test_unknown_index_structure_is_a_config_error():
    config = load_config()
    config["runs"][0]["index"]["structure"] = "skip_list"
    with pytest.raises(ConfigError):
        new_runner()(config)


def test_unknown_retrieval_type_is_a_config_error():
    config = load_config()
    config["runs"][0]["retrieval"]["type"] = "bm25"
    with pytest.raises(ConfigError):
        new_runner()(config)


def test_unknown_analysis_component_is_a_config_error():
    config = load_config()
    config["runs"][0]["analysis"]["tokenizer"]["type"] = "ngram"
    with pytest.raises(ConfigError):
        new_runner()(config)


def test_missing_dataset_file_is_a_data_error(tmp_path, monkeypatch):
    from ir_lab.persistence.dataset import dataset_registry

    monkeypatch.setattr(
        dataset_registry.DatasetRegistry,
        "loaders",
        {"toy": lambda: dataset_registry._load_json(str(tmp_path / "missing.json"))},
    )
    with pytest.raises(DataError):
        DatasetStore().load("toy")


def test_unsupported_boolean_operator_is_an_unsupported_feature_error():
    from ir_lab.processing.boolean.boolean_evaluator import BooleanEvaluator
    from ir_lab.processing.boolean.boolean_retriever import BooleanRetriever
    from ir_lab.test.fixtures import Fixtures

    evaluator = BooleanEvaluator(BooleanRetriever(Fixtures.inverted_index()))
    with pytest.raises(UnsupportedFeatureError):
        evaluator.evaluate_binary("near", [1], [2])
