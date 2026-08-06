from ir_lab.models.queries import AnalyzedQuery,BooleanRPNQuery
from .query_parser import QueryParser
from .fragment import Fragment
import re
class BooleanRPNParser(QueryParser):
    def __init__(self):
        self.operators = {
            'and': 1,
            'or': 1,
            'not': 2
        }

    def parse(self,query: list[Fragment]) -> list[Fragment]:
        input = self.tokenize(query)

        holding_stack = []
        output_stack = []
        for fragment in input:
            term = fragment.content
            if term not in self.operators:
                output_stack.append(fragment)
            else:
                while (holding_stack and holding_stack[-1] != '(' and
                       self.operators[holding_stack[-1]] >= self.operators[term]):
                    output_stack.append(holding_stack.pop())
                holding_stack.append(fragment)
        while holding_stack:
            output_stack.append(holding_stack.pop())

        return output_stack


    def tokenize(self,query : str) -> list[str] : 
        token_specification = [
        ('OP',    r'\b(?:and|or|not)\b'),
        ('TERM',  r'[^\s()]+'),
        ('SKIP',  r'[\s\t]+'),
        ]
        tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
        tokens = []

        for mo in re.finditer(tok_regex, query):
            kind = mo.lastgroup
            value = mo.group()
            if kind != 'SKIP':
                tokens.append(Fragment(kind, value))
        return tokens



        
    def __call__(self, query : AnalyzedQuery):
        return self.parse(query)


if __name__ == "__main__":
    
    from ir_lab.test import Fixtures

    text = "information.retrieval and cookies"
    parser = BooleanRPNParser()
    print(parser(text))

    """        
    analyzed_query = Fixtures.analyzed_query()
    parser =  BooleanRPNParser()
    rpn_query = parser(analyzed_query)
    print(rpn_query.stack)
    """

    