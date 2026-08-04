from .base_index import BaseIndex
class IncidenceMatrix(BaseIndex):


    def add_term(self,term) : 
        self.vocabulary[term] = len(self.vocabulary)
        self.matrix.append([0] * len(self.documents))

    def set_incidence(self,term,doc_id):
        row = self.vocabulary[term]
        self.matrix[row][doc_id] = 1
