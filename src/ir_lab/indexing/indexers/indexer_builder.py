from .inverted_indexer import InvertedIndexer
from .incidence_matrix_indexer import IncidenceMatrixIndexer
from ir_lab.errors import ConfigError

INDEXERS = {
    "inverted": InvertedIndexer,
    "incidence_matrix": IncidenceMatrixIndexer,
}


class IndexerBuilder:

    def build(self, config: dict):
        try:
            structure = config["structure"]
        except KeyError:
            raise ConfigError(f"index config is missing a 'structure' field: {config!r}")

        try:
            cls = INDEXERS[structure]
        except KeyError:
            raise ConfigError(
                f"unknown index structure {structure!r}; expected one of {sorted(INDEXERS)}"
            )
        return cls()

    def __call__(self, config: dict):
        return self.build(config)
