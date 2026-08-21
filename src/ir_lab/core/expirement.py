
from dataclasses import dataclass
from ir_lab.models.datasets import Dataset
from .run import Run

@dataclass
class Expirement :
    dataset : Dataset
    runs : list[Run]
    #evaluation : list[dict] : kept away for now