from .inverted_indexer import InvertedIndexer
from .incidence_matrix_indexer import IncidenceMatrixIndexer

INDEXERS = {
    "inverted": InvertedIndexer,
    "incidence_matrix": IncidenceMatrixIndexer,
}


class IndexerBuilder:

    def build(self, config: dict):
        try:
            cls = INDEXERS[config["structure"]]
        except KeyError:
            raise ValueError(f"Unsupported index structure: {config.get('structure')!r}")
        return cls()

    def __call__(self, config: dict):
        return self.build(config)
