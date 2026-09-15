from .dataset_registry import DatasetRegistry
from ir_lab.models.datasets import Dataset

class DatasetStore :

    def __init__(self):
        pass

    def load(self, dataset : str) -> Dataset :
        loader = DatasetRegistry.get_loader(dataset)
        if loader is None:
            raise ValueError(f"Unknown dataset: {dataset!r}")
        return loader()
