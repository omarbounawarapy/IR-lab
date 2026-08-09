from ir_lab.models.queries import Query
from ir_lab.models.documents import ScoredDocument
from ir_lab.analyzing.analyzers import analyzer,QueryAnalyzer
from ir_lab.indexing.indexes.base_index import BaseIndex
from abc import ABC , abstractmethod

class QueryProcessor(ABC) : 
    def __init__(self,analyzer : analyzer, index : BaseIndex):
        self.analyzer = QueryAnalyzer(analyzer)
        self.index = index

    @abstractmethod
    def process(query : Query) -> list[ScoredDocument] : 
        pass