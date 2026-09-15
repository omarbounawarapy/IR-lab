from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ir_lab.analyzing.analyzers import QueryAnalyzer

from ir_lab.models.queries import Query
from ir_lab.models.documents import ScoredDocument

from abc import ABC , abstractmethod

from dataclasses import dataclass

@dataclass
class BaseProcessor(ABC) :     
    query_analyzer : QueryAnalyzer 


    @abstractmethod
    def process(self,query : Query) -> list[ScoredDocument] : 
        pass
    


    def __call__(self,queries:list[Query]) -> list[list[ScoredDocument]] :

        results =[]
        for query in queries :
            result = self.process(query)
            results.append(result)
        return results
