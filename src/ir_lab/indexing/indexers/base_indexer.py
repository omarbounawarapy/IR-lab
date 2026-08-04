from abc import abstractmethod,ABC
from ir_lab.indexing.indexes import BaseIndex
from ir_lab.models.documents import AnalyzedDocument

class BaseIndexer(ABC) : 
    def __init__(self):
        pass

    @abstractmethod
    def index(self,docs:list[AnalyzedDocument]) -> BaseIndex:
        pass 

    def __call__(self, docs: list[AnalyzedDocument]) -> BaseIndex :
        return self.index(docs)