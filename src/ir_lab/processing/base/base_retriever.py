
from abc import ABC,abstractmethod

from ir_lab.models.queries import ExecutableQuerry
from ir_lab.indexing.indexes import BaseIndex
from ir_lab.models.documents import ScoredDocument

class Retriver(ABC):
    def __init__(self, index: BaseIndex):
        self.index = index


    @abstractmethod
    def retrieve(self, query: ExecutableQuerry  ) -> list[ScoredDocument]:
        pass