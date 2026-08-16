
from abc import ABC,abstractmethod

from ir_lab.models.queries import ExecutableQuerry
from ir_lab.indexing.indexes import BaseIndex

class Retriver(ABC):
    def __init__(self, index: BaseIndex):
        self.index = index


    @abstractmethod
    def retrieve(self, query: ExecutableQuerry  ) -> list[Document]:
        pass