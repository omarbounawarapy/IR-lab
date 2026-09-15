import uuid
from datetime import datetime, timezone

from ir_lab.provenance import get_code_version


def build_run_record(
    experiment_id,
    run_config_id,
    run_config: dict,
    dataset_id: str,
    queries: list,
    run_results: list,
    seed=None,
    evaluation=None,
    ranked_evaluation=None,
) -> dict:
    """A self-contained, structurally-linked record of one executed run:
    its own config, the code version that produced it, and its results
    all live in the same record -- not filename-adjacent files that a
    rename could silently disconnect."""
    return {
        "run_id": uuid.uuid4().hex,
        "experiment_id": experiment_id,
        "run_config_id": run_config_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "code_version": get_code_version(),
        "seed": seed,
        "dataset_id": dataset_id,
        "config": run_config,
        "queries": [query.id for query in queries],
        "retrieved": [[doc.id for doc in docs] for docs in run_results],
        "evaluation": evaluation,
        "ranked_evaluation": ranked_evaluation,
    }
