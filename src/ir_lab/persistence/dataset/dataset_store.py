from .dataset_registry import DatasetRegistry
from ir_lab.models.datasets import Dataset
from ir_lab.errors import ConfigError

class DatasetStore :

    def __init__(self):
        pass

    def load(self, dataset : str) -> Dataset :
        loader = DatasetRegistry.get_loader(dataset)
        if loader is None:
            raise ConfigError(
                f"unknown dataset {dataset!r}; "
                f"expected one of {sorted(DatasetRegistry.loaders)}"
            )
        return loader()
