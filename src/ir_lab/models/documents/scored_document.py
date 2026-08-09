from dataclasses import dataclass

@dataclass
class ScoredDocument :
    id : int 
    rsv : float | None = None
    position : int = 0
    meta : dict = {}
