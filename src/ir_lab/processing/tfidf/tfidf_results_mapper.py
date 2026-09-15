from ir_lab.models.documents import ScoredDocument
from ..base.base_mapper import BaseMapper


class TFIDFResultsMapper(BaseMapper):

    @staticmethod
    def map_results(scored_pairs: list[tuple]) -> list[ScoredDocument]:
        return [
            ScoredDocument(doc_id, rsv=score, position=position)
            for position, (doc_id, score) in enumerate(scored_pairs)
        ]
