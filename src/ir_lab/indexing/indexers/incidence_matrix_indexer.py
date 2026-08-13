from ir_lab.models.documents import AnalyzedDocument
from ir_lab.indexing.indexes import IncidenceMatrix
from .base_indexer import BaseIndexer

class IncidenceMatrixIndexer(BaseIndexer):

    def index(self, docs: list[AnalyzedDocument]) -> IncidenceMatrix:
        
        matrix = IncidenceMatrix(size=len(docs))

        for doc_id, doc in enumerate(docs):
            for term in doc.term_set():
                if not matrix.in_vocabulary(term):
                    matrix.add_term(term)
                matrix.set_incidence(term,doc_id)

        matrix.sort_vocabulary()

        return matrix

    




if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    docs = Fixtures.analyzed_documents()
    indexer = IncidenceMatrixIndexer()
    index = indexer(docs)
    print(index)


