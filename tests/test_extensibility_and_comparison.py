"""Extensibility and comparison acceptance tests: a second retrieval model (TF-IDF) is added
purely additively -- proven by a diff check, not just claimed -- and two
runs differing only in retrieval model produce a real side-by-side
comparison; a comparison across something undeclared is caught, not
silently accepted.
"""
import json
from pathlib import Path

import pytest

from ir_lab.core import ExpirimentRunner
from ir_lab.core.comparison import compare_runs
from ir_lab.errors import ConfigError
from ir_lab.persistence.dataset.dataset_store import DatasetStore
from ir_lab.persistence.index.index_store import IndexStore
from ir_lab.persistence.run.run_store import RunStore


def load_config():
    return json.load(open("experiments/configs/toy_boolean_vs_tfidf.json"))


def test_tfidf_ranks_by_score_descending():
    from ir_lab.analyzing.analyzers import AnalyzerBuilder, DocumentAnalyzer
    from ir_lab.indexing.indexers.inverted_indexer import InvertedIndexer
    from ir_lab.processing.processor_builder import ProcessorBuilder
    from ir_lab.models.queries import Query

    analyzer_config = {
        "character_filters": [{"type": "ponctuation", "replace": " "}],
        "tokenizer": {"type": "space"},
        "token_filters": [{"type": "lowercase"}],
    }
    analyzer = AnalyzerBuilder().build(analyzer_config)
    dataset = DatasetStore().load("toy")
    doc_analyzer = DocumentAnalyzer(analyzer)
    index = InvertedIndexer()([doc_analyzer(d) for d in dataset.corpus])

    processor = ProcessorBuilder()({"type": "tfidf"}, analyzer, index)
    result = processor([Query(id=0, content="vector")])[0]

    import math
    # "vector" occurs once, in doc 3 only, of 6 documents -- tf=1, idf=ln(6/1).
    assert result[0].id == 3
    assert result[0].rsv == pytest.approx(math.log(6))


def test_tfidf_required_no_special_casing_in_base_indexing_or_analyzing():
    # The point of this test: adding a second retrieval model didn't
    # require indexing/, analyzing/, or processing/base/ to know TF-IDF
    # exists. If any of them mention it, the abstraction didn't generalize
    # -- it was special-cased instead.
    root = Path("src/ir_lab")
    forbidden_dirs = [root / "indexing", root / "analyzing", root / "processing" / "base"]
    for directory in forbidden_dirs:
        for path in directory.rglob("*.py"):
            text = path.read_text().lower()
            assert "tfidf" not in text and "tf-idf" not in text, (
                f"{path} references TF-IDF -- indicates special-casing, not generalization"
            )


def test_boolean_vs_tfidf_controlled_comparison(tmp_path):
    run_store = RunStore(root=str(tmp_path))
    runner = ExpirimentRunner(DatasetStore(), IndexStore(), run_store=run_store)
    runner(load_config())

    records = {run_store.load(rid)["run_config_id"]: run_store.load(rid) for rid in run_store.list()}
    comparison = compare_runs(records["boolean_run"], records["tfidf_run"], varying={"retrieval"})

    assert comparison["varying"] == ["retrieval"]
    assert comparison["metrics_a"] is not None
    assert comparison["metrics_b"] is not None


def test_comparison_flags_an_undeclared_difference(tmp_path):
    run_store = RunStore(root=str(tmp_path))
    runner = ExpirimentRunner(DatasetStore(), IndexStore(), run_store=run_store)

    config = load_config()
    # sabotage: also change the analysis of the second run, without
    # declaring "analysis" as a varying dimension.
    config["runs"][1]["analysis"]["character_filters"] = []
    runner(config)

    records = {run_store.load(rid)["run_config_id"]: run_store.load(rid) for rid in run_store.list()}
    with pytest.raises(ConfigError):
        compare_runs(records["boolean_run"], records["tfidf_run"], varying={"retrieval"})
