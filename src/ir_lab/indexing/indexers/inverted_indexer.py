from .base_indexer import BaseIndexer
from ir_lab.models.documents import AnalyzedDocument
from ir_lab.indexing.indexes import InvertedIndex

class InvertedIndexer(BaseIndexer):
    def index(self,docs:list[AnalyzedDocument]) -> InvertedIndex:
        terms = []
        for doc in docs :
            doc_id = doc.document.id
            positions = {}
            for token in doc.tokens : 
                term = token.content
                position = token.position
                if term in positions:
                    positions[term].append(position)
                else : 
                    positions[term] = [position]
            for term in positions:
                terms.append(
                    (term,
                    doc_id,
                    positions[term])
                )

        terms = sorted(terms)
        InvInd = InvertedIndex()

        for term,doc_id,positions in terms :
            InvInd.add_posting(term,doc_id,positions)

        return InvInd
    
        
if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    docs = Fixtures.analyzed_documents()
    indexer = InvertedIndexer()
    index = indexer(docs)
    print(index)
