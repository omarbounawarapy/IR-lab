from  ir_lab.models.queries import Query
from ir_lab.models.queries  import ExecutableQuery 
from abc import abstractmethod,ABC

class QueryParser(ABC):
    @abstractmethod
    def parse(self, query:Query) -> ExecutableQuery:
        pass

    def __call__(self,query:Query) -> ExecutableQuery:
        return self.parse(query)