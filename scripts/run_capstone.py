"""Capstone worked example.

Research question: does disabling punctuation filtering change TF-IDF
retrieval effectiveness (MAP) on the CISI collection?

Runs both configs in experiments/capstone/, persists both runs (with
their embedded config, code version, and evaluation) into
experiments/capstone/runs/, writes the controlled comparison +
significance test to experiments/capstone/comparison.json, and prints
a conclusion. No framework code is touched by this script -- it is
pure configuration plus the framework's own runner and comparison
tools, exactly as required.
"""
import json
from pathlib import Path

from ir_lab.core import ExpirimentRunner
from ir_lab.core.comparison import compare_runs
from ir_lab.persistence.dataset.dataset_store import DatasetStore
from ir_lab.persistence.index.index_store import IndexStore
from ir_lab.persistence.run.run_store import RunStore

CAPSTONE_DIR = Path(__file__).resolve().parent.parent / "experiments" / "capstone"


def main():
    run_store = RunStore(root=str(CAPSTONE_DIR / "runs"))
    runner = ExpirimentRunner(DatasetStore(), IndexStore(), run_store=run_store)

    with_filter = json.load(open(CAPSTONE_DIR / "cisi_tfidf_with_punctuation_filter.json"))
    without_filter = json.load(open(CAPSTONE_DIR / "cisi_tfidf_without_punctuation_filter.json"))

    runner(with_filter)
    runner(without_filter)

    records_by_run_config_id = {}
    for run_id in run_store.list():
        record = run_store.load(run_id)
        records_by_run_config_id[record["run_config_id"]] = record

    comparison = compare_runs(
        records_by_run_config_id["with_punctuation_filter"],
        records_by_run_config_id["without_punctuation_filter"],
        varying={"analysis"},
    )

    with open(CAPSTONE_DIR / "comparison.json", "w") as f:
        json.dump(comparison, f, indent=2, sort_keys=True)

    print(json.dumps(comparison, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
