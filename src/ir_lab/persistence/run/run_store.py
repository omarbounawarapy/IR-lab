import json
from pathlib import Path

from ir_lab.errors import DataError


class RunStore:
    """Flat, JSON-file-per-run persistence, keyed by run id.

    Each stored record embeds its own resolved config, dataset id, code
    version, seed, queries, retrieved results and (optionally)
    evaluation -- the config/result link is structural (part of the one
    file), not filename-adjacent convention that a rename could break.
    """

    def __init__(self, root: str = "runs"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, run_id: str) -> Path:
        return self.root / f"{run_id}.json"

    def save(self, record: dict) -> str:
        run_id = record["run_id"]
        with open(self._path(run_id), "w") as f:
            json.dump(record, f, indent=2, sort_keys=True)
        return run_id

    def load(self, run_id: str) -> dict:
        try:
            with open(self._path(run_id)) as f:
                return json.load(f)
        except FileNotFoundError:
            raise DataError(f"no run found with id {run_id!r}")

    def exists(self, run_id: str) -> bool:
        return self._path(run_id).exists()

    def list(self) -> list[str]:
        return sorted(p.stem for p in self.root.glob("*.json"))
