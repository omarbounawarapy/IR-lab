"""Black-box worker for the case study: runs one experiment config through
the framework's own public entry points (ExpirimentRunner + stores) exactly
as scripts/run_capstone.py does, and times it from the outside.

Invoked as its own subprocess (one config per process) so that the parent
driver can measure this process's peak RSS in isolation via `/usr/bin/time
-v`, rather than a running max shared across configs. No framework internals
are touched -- only the same public API a script author would use.

Runs the config twice in-process:
  1. cold  -- index does not exist yet, so this includes index build time.
  2. warm  -- same ExpirimentRunner/IndexStore instance, so the in-memory
              index from step 1 is reused and this isolates retrieval-only
              latency.

Writes a single JSON result (timings + the run records) to the output path
given as argv[2]. Any exception is caught and reported as a structured
failure instead of a bare traceback, since a crash is itself a valid
black-box finding.
"""
import json
import sys
import time
import traceback
from pathlib import Path

from ir_lab.core import ExpirimentRunner
from ir_lab.persistence.dataset.dataset_store import DatasetStore
from ir_lab.persistence.index.index_store import IndexStore
from ir_lab.persistence.run.run_store import RunStore


def main():
    config_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    run_store_dir = Path(sys.argv[3])

    config = json.loads(config_path.read_text())
    run_store = RunStore(root=str(run_store_dir))
    dataset_store = DatasetStore()
    index_store = IndexStore()

    # Cold run persists the record (this is the one committed to runs/).
    # Warm run shares the same in-memory index_store (so it reuses the
    # index just built) but is given no run_store, since it would only
    # write a near-duplicate record under a fresh uuid.
    cold_runner = ExpirimentRunner(dataset_store, index_store, run_store=run_store)
    warm_runner = ExpirimentRunner(dataset_store, index_store, run_store=None)

    result = {"config_id": config["meta"]["id"], "ok": False}

    try:
        t0 = time.perf_counter()
        cold_runner(config)
        t1 = time.perf_counter()
        warm_runner(config)
        t2 = time.perf_counter()

        run_config_id = config["runs"][0]["id"]
        record = None
        for run_id in run_store.list():
            candidate = run_store.load(run_id)
            if candidate["run_config_id"] == run_config_id:
                record = candidate

        # The full record (incl. per-query retrieved doc ids) already lives
        # in run_store; this result file only needs the summary fields.
        record_summary = {k: v for k, v in record.items() if k != "retrieved"}
        record_summary["num_retrieved_total"] = sum(len(r) for r in record["retrieved"])

        result.update({
            "ok": True,
            "cold_total_s": t1 - t0,
            "warm_retrieval_s": t2 - t1,
            "indexing_only_s": (t1 - t0) - (t2 - t1),
            "run_record": record_summary,
        })
    except Exception as exc:
        result.update({
            "ok": False,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "traceback": traceback.format_exc(),
        })

    output_path.write_text(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
