from .base_index import BaseIndex
class IncidenceMatrix(BaseIndex):

    def __init__(self,size):
        super().__init__()
        self.matrix = []
        self.size = size

    def add_term(self,term) :
        self.vocabulary[term] = len(self.vocabulary)
        self.matrix.append([0] * self.size)

    def set_incidence(self,term,doc_id):
        row = self.vocabulary[term]
        self.matrix[row][doc_id] = 1

    def __repr__(self):
        return (
            f"IncidenceMatrix("
            f"vocabulary={self.vocabulary!r}, "
            f"matrix={self.matrix!r}"
            f")"
        )