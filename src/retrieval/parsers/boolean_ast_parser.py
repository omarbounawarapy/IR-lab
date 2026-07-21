from models.queries import Query
from models.excutable_queries import BooleanASTQuery
class BooleanASTParser(QueryParser):
    def transform(self, query: Query) -> BooleanASTQuery:
        pass