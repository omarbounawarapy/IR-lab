from ir_lab.models.documents import ScoredDocument


class BooleanResultsMapper : 
    def __init__(self):
        pass 

    @staticmethod
    def map_results(docs :list[int]) -> list[ScoredDocument] : 
        results = []
        for id in docs :
            doc = ScoredDocument(id)
            results.append(doc)
        return results

    def __call__(self, docs : list[int]) -> list[ScoredDocument]:
        return self.map_results(docs)