from ir_lab.models.queries import AnalyzedQuery,BooleanRPNQuery
from .query_parser import QueryParser
class BooleanRPNParser(QueryParser):
    def __init__(self):
        self.operators = {
            'and': 1,
            'or': 1,
            'not': 2
        }

    def parse(self,query: AnalyzedQuery) -> BooleanRPNQuery:
        input = query.tokens
        holding_stack = []
        output_stack = []
        for token in input:
            term = token.content
            if term not in self.operators:
                output_stack.append(term)
            else:
                while (holding_stack and holding_stack[-1] != '(' and
                       self.operators[holding_stack[-1]] >= self.operators[term]):
                    output_stack.append(holding_stack.pop())
                holding_stack.append(term)
        while holding_stack:
            output_stack.append(holding_stack.pop())

   
        return BooleanRPNQuery(
            query=query,
            stack=output_stack,
        )
    def __call__(self, query : AnalyzedQuery):
        return self.parse(query)


if __name__ == "__main__":
    
    from ir_lab.test import Fixtures

        
    analyzed_query = Fixtures.analyzed_query()
    parser =  BooleanRPNParser()
    rpn_query = parser(analyzed_query)
    print(rpn_query.stack)


    