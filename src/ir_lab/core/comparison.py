from ir_lab.errors import ConfigError
from ir_lab.evaluation.significance import paired_t_test


def compare_runs(record_a: dict, record_b: dict, varying: set) -> dict:
    """Compares two persisted run records under the L8 controlled-
    comparison rule: every field is required to be identical except the
    dimensions declared in `varying`. Raises ConfigError -- not a
    silently-misleading comparison table -- the moment something
    undeclared also differs (a different dataset, a different query
    set, an unrelated config field).

    When both runs carry rank-aware (MAP/MRR/nDCG) per-query evaluation
    over the same topics, also runs a paired t-test on their per-topic
    average precision -- so "System A beats System B" comes with the
    significance test backing it, not just two numbers side by side.
    """

    for field in ("dataset_id", "queries"):
        if record_a[field] != record_b[field]:
            raise ConfigError(
                f"cannot compare runs {record_a['run_id']!r} and {record_b['run_id']!r}: "
                f"{field!r} differs ({record_a[field]!r} vs {record_b[field]!r}) "
                f"but was not declared as the varying dimension"
            )

    config_a, config_b = record_a["config"], record_b["config"]
    always_allowed_to_differ = varying | {"id"}  # each run declares its own identity
    for key in set(config_a) | set(config_b):
        if key in always_allowed_to_differ:
            continue
        if config_a.get(key) != config_b.get(key):
            raise ConfigError(
                f"cannot compare runs {record_a['run_id']!r} and {record_b['run_id']!r}: "
                f"config field {key!r} differs but was not declared as the varying "
                f"dimension ({sorted(varying)}) -- this would not be a controlled comparison"
            )

    comparison = {
        "run_a": record_a["run_id"],
        "run_b": record_b["run_id"],
        "varying": sorted(varying),
        "metrics_a": _aggregate(record_a.get("evaluation")),
        "metrics_b": _aggregate(record_b.get("evaluation")),
        "ranked_metrics_a": _aggregate(record_a.get("ranked_evaluation")),
        "ranked_metrics_b": _aggregate(record_b.get("ranked_evaluation")),
        "significance": None,
    }

    ranked_a, ranked_b = record_a.get("ranked_evaluation"), record_b.get("ranked_evaluation")
    if ranked_a and ranked_b and len(ranked_a) >= 2:
        ap_a = [q["ap"] for q in ranked_a]
        ap_b = [q["ap"] for q in ranked_b]
        comparison["significance"] = {"metric": "ap", **paired_t_test(ap_a, ap_b)}

    return comparison


def _aggregate(evaluation):
    if not evaluation:
        return None
    metric_names = [key for key in evaluation[0] if key != "query_id"]
    return {
        name: sum(query[name] for query in evaluation) / len(evaluation)
        for name in metric_names
    }
