from models.queries import Query
from models.excutable_queries import ExecutableQuery

@abstractclass
class QueryParser(ABC):
    @abstractmethod
    def transform(self, query:Query) -> ExecutableQuery:
        pass