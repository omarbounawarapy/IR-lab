
from abc import ABC

from information_retrival_lab.src.core.models.excutable_querries.executable_querry import ExecutableQuerry

@abstractclass
class Retriver(ABC):
    def __init__(self, index: Index):
        self.index = index


    @abstractmethod
    def retrieve(self, query: ExecutableQuerry  ) -> list[Document]:
        pass