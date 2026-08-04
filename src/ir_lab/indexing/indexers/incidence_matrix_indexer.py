from ir_lab.models.documents import AnalyzedDocument
from ir_lab.indexing.indexes import IncidenceMatrix

class IncidenceMatrixIndexer:
    def index(self, docs: list[AnalyzedDocument]) -> IncidenceMatrix:
    
        matrix = IncidenceMatrix()

        for doc_id, doc in enumerate(docs):
            for token in set(doc.tokens):
                term = token.content

                if not matrix.in_vocabulary(term):
                    matrix.add_term(term)


                matrix.set_incidence(term,doc_id)

        return matrix
