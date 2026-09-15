from ir_lab.models.documents import ScoredDocument
from ..base.base_mapper import BaseMapper


class BooleanResultsMapper(BaseMapper) :
    def __init__(self):
        pass

    @staticmethod
    def map_results(docs :list[int]) -> list[ScoredDocument] :
        results = []
        for position, id in enumerate(docs) :
            doc = ScoredDocument(id, position=position)
            results.append(doc)
        return results
