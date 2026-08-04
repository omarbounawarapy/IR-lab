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

    def sort_vocabulary(self):
        sorted_terms = sorted(self.vocabulary)
        
        new_vocabulary = {}
        new_matrix = []
        
        for new_row, term in enumerate(sorted_terms):
            old_row = self.vocabulary[term]
            new_vocabulary[term] = new_row
            new_matrix.append(self.matrix[old_row])
        
        self.vocabulary = new_vocabulary
        self.matrix = new_matrix

    def __repr__(self):
        return (
            f"IncidenceMatrix("
            f"vocabulary={self.vocabulary!r}, "
            f"matrix={self.matrix!r}"
            f")"
        )