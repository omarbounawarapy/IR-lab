from ..fragments.fragment import Fragment
import re
from .rpn_stack import RPNStack

class RPNParser : 

    def parse(self,text : str) -> RPNStack:
        input = self.tokenize(text)
        holding_stack = []
        rpn = RPNStack()
        for fragment in input:
            term = fragment.content
            if term not in self.operators:
                rpn.push(fragment)
            else:
                while holding_stack and holding_stack[-1].content != '(' and self.precedence(holding_stack[-1].content) >= self.precdence(term):
                    rpn.push(holding_stack.pop())
                holding_stack.append(fragment)
        while holding_stack:
            rpn.push(holding_stack.pop())

        return rpn


    def precedence(self,operator:str):
        return self.operators[operator]["precedence"]

    def fragment_class(self,operator:str):
        return self.operators[operator]["class"]


    def tokenize(self,query : str) -> list[str] : 

        tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification)
        tokens = []

        for mo in re.finditer(tok_regex, query):
            type = mo.lastgroup
            value = mo.group()
            if type != 'SKIP':
                tokens.append(Fragment(type, value))
        return tokens

    def __call__(self, query : str) -> RPNStack:
        return self.parse(query)



    