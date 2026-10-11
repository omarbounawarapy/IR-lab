from abc import ABC, abstractmethod

from ir_lab.models.queries import ExecutableQuery, Query


class BaseParser(ABC):
    @abstractmethod
    def parse(self, query:Query) -> ExecutableQuery:
        pass

    def __call__(self,query:Query) -> ExecutableQuery:
        return self.parse(query)