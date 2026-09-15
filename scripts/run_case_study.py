"""Case study driver: black-box test of the framework on the CISI collection.

For each config in experiments/case_study/*.json, this script shells out to
scripts/case_study_worker.py -- one fresh subprocess per config, wrapped in
`/usr/bin/time -v` -- so that:

  - runtime is measured from outside the framework (wall clock around the
    whole process), and
  - peak memory (max RSS) is isolated per config, since a shared long-lived
    process would only ever report a running maximum across configs.

No framework internals are touched anywhere in this file or in the worker --
only ExpirimentRunner/DatasetStore/IndexStore/RunStore, the same public
surface scripts/run_capstone.py uses. Effectiveness numbers, timings, and
memory usage are all collected into experiments/case_study/results.json.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASE_STUDY_DIR = ROOT / "experiments" / "case_study"
RUNS_DIR = CASE_STUDY_DIR / "runs"
WORKER = ROOT / "scripts" / "case_study_worker.py"

CONFIGS = [
    CASE_STUDY_DIR / "cisi_tfidf.json",
    CASE_STUDY_DIR / "cisi_boolean.json",
]

MAXRSS_RE = re.compile(r"Maximum resident set size \(kbytes\):\s*(\d+)")
ELAPSED_RE = re.compile(r"Elapsed \(wall clock\) time.*?:\s*([\d:.]+)")


def _parse_elapsed(value: str) -> float:
    parts = value.split(":")
    parts = [float(p) for p in parts]
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + part
    return seconds


def run_one(config_path: Path) -> dict:
    output_path = config_path.with_suffix(".result.json")
    time_log = config_path.with_suffix(".time.log")

    cmd = [
        "/usr/bin/time", "-v", "-o", str(time_log),
        sys.executable, str(WORKER), str(config_path), str(output_path), str(RUNS_DIR),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)

    time_text = time_log.read_text()
    maxrss_kb = int(MAXRSS_RE.search(time_text).group(1))
    elapsed_s = _parse_elapsed(ELAPSED_RE.search(time_text).group(1))

    worker_result = json.loads(output_path.read_text())

    return {
        "config": config_path.name,
        "process_elapsed_s": elapsed_s,
        "process_peak_rss_kb": maxrss_kb,
        **worker_result,
    }


def summarize(entry: dict) -> dict:
    if not entry["ok"]:
        return {
            "config": entry["config"],
            "ok": False,
            "error_type": entry["error_type"],
            "error_message": entry["error_message"],
            "process_elapsed_s": entry["process_elapsed_s"],
            "process_peak_rss_kb": entry["process_peak_rss_kb"],
        }

    record = entry["run_record"]
    evaluation = record.get("evaluation") or []
    ranked = record.get("ranked_evaluation") or []

    def _mean(rows, key):
        return sum(r[key] for r in rows) / len(rows) if rows else None

    return {
        "config": entry["config"],
        "ok": True,
        "run_config_id": record["run_config_id"],
        "dataset_id": record["dataset_id"],
        "num_queries": len(record["queries"]),
        "num_documents_retrieved_total": record["num_retrieved_total"],
        "effectiveness": {
            "precision": _mean(evaluation, "precision"),
            "recall": _mean(evaluation, "recall"),
            "f1": _mean(evaluation, "f1"),
            "map": _mean(ranked, "ap"),
            "mrr": _mean(ranked, "rr"),
            "ndcg@10": _mean(ranked, "ndcg@10"),
        },
        "performance": {
            "process_elapsed_s": entry["process_elapsed_s"],
            "process_peak_rss_kb": entry["process_peak_rss_kb"],
            "cold_total_s": entry["cold_total_s"],
            "indexing_only_s": entry["indexing_only_s"],
            "warm_retrieval_s": entry["warm_retrieval_s"],
        },
    }


def main():
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    entries = [run_one(cfg) for cfg in CONFIGS]
    summary = [summarize(e) for e in entries]

    results_path = CASE_STUDY_DIR / "results.json"
    results_path.write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
