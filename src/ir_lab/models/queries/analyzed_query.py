from .query import Query
class AnalyzedQuery: 
    def __init__(self,query: Query,tokens):
        self.query = query
        self.tokens = tokens
        