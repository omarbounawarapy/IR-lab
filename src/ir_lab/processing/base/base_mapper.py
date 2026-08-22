from abc import ABC , abstractmethod
from typing import Any
from ir_lab.models.documents import ScoredDocument


class BaseMapper(ABC): 

    @abstractmethod
    def map_results(docs : list[Any]) -> ScoredDocument :
        pass 

    def __call__(self, docs : list[Any]) -> list[ScoredDocument]:
          return self.map_results(docs)