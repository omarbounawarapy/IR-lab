"""Happy-path acceptance tests: a real boolean query, over the real toy corpus on
disk, produces a correct, independently-verifiable result through IR Lab's
own code -- no fixtures standing in for ingestion, analysis or indexing.
"""
import json

import pytest

from ir_lab.analyzing.analyzers import AnalyzerBuilder, DocumentAnalyzer
from ir_lab.core import ExpirimentRunner
from ir_lab.indexing.indexers.inverted_indexer import InvertedIndexer
from ir_lab.models.queries import Query
from ir_lab.persistence.dataset.dataset_store import DatasetStore
from ir_lab.persistence.index.index_store import IndexStore
from ir_lab.processing.processor_builder import ProcessorBuilder

ANALYZER_CONFIG = {
    "character_filters": [{"type": "ponctuation", "replace": " "}],
    "tokenizer": {"type": "space"},
    "token_filters": [{"type": "lowercase"}],
}


@pytest.fixture(scope="module")
def toy_index():
    dataset = DatasetStore().load("toy")
    analyzer = AnalyzerBuilder().build(ANALYZER_CONFIG)
    document_analyzer = DocumentAnalyzer(analyzer)
    analyzed_docs = [document_analyzer(doc) for doc in dataset.corpus]
    return InvertedIndexer()(analyzed_docs), analyzer


@pytest.fixture(scope="module")
def toy_processor(toy_index):
    index, analyzer = toy_index
    return ProcessorBuilder()({"type": "boolean"}, analyzer, index)


def run_query(processor, text):
    result = processor([Query(id=0, content=text)])[0]
    return [doc.id for doc in result]


def test_every_submodule_imports():
    import importlib
    import pkgutil

    import ir_lab

    for _, name, _ in pkgutil.walk_packages(ir_lab.__path__, prefix="ir_lab."):
        importlib.import_module(name)


def test_inverted_index_resolves_real_document_identities(toy_index):
    index, _ = toy_index
    # "index" appears (post-lowercasing) in doc 1 and doc 5 of the real
    # toy corpus on disk -- verifiable by reading datasets/toy/dataset.json.
    assert index.get_term_documents("index") == [1, 5]


def test_single_operator_query(toy_processor):
    assert run_query(toy_processor, "index and posting") == [1, 5]


def test_two_operator_query_respects_precedence(toy_processor):
    # (index and posting) or vector -- AND binds tighter than OR.
    assert run_query(toy_processor, "index and posting or vector") == [1, 3, 5]


def test_not_query(toy_processor):
    # complement of {vector} = {3} over the real 6-document corpus.
    assert run_query(toy_processor, "not vector") == [1, 2, 4, 5, 6]


def test_combined_not_and_query(toy_processor):
    assert run_query(toy_processor, "index and not posting") == []


def test_config_driven_execution_matches_hand_computed_result():
    config = json.load(open("experiments/configs/toy_inverted_index.json"))
    runner = ExpirimentRunner(DatasetStore(), IndexStore())
    results = runner(config)

    example = results["example"]
    assert [doc.id for doc in example[0]] == [1, 5]  # "index and posting"
    assert [doc.id for doc in example[1]] == [2, 3]  # "boolean or vector"
    assert [doc.id for doc in example[2]] == []      # "retrieval and vector"


def test_repeated_runs_are_identical():
    config = json.load(open("experiments/configs/toy_inverted_index.json"))
    first = ExpirimentRunner(DatasetStore(), IndexStore())(config)
    second = ExpirimentRunner(DatasetStore(), IndexStore())(config)

    first_ids = [[doc.id for doc in r] for r in first["example"]]
    second_ids = [[doc.id for doc in r] for r in second["example"]]
    assert first_ids == second_ids
