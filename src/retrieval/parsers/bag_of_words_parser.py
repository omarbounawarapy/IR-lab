from models.queries import Query
from models.excutable_queries import ExecutableQuery

class BagOfWordsParser(Querryparser):
    def transform(self, query: Query) -> ExecutableQuery:
        pass
    
