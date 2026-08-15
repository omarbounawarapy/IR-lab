from dataclasses import dataclass, field

@dataclass
class ScoredDocument:
    id: int
    rsv: float | None = None
    position: int = 0
    meta: dict = field(default_factory=dict)