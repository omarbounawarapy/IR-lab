from abc import ABC ,abstractmethod
from .fragment import Fragment
import re

class RPNParser(ABC) : 

    def parse(self,text : str) -> list[Fragment]:
        input = self.tokenize(text)
        holding_stack = []
        output_stack = []
        for fragment in input:
            term = fragment.content
            if term not in self.operators:
                output_stack.append(fragment)
            else:
                while holding_stack and holding_stack[-1].content != '(' and self.precedence(holding_stack[-1].content) >= self.precdence(term):
                    output_stack.append(holding_stack.pop())
                holding_stack.append(fragment)
        while holding_stack:
            output_stack.append(holding_stack.pop())

        return output_stack


    def precedence(self,operator:str):
        return self.operators[operator]


    def tokenize(self,query : str) -> list[str] : 

        tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification)
        tokens = []

        for mo in re.finditer(tok_regex, query):
            kind = mo.lastgroup
            value = mo.group()
            if kind != 'SKIP':
                tokens.append(Fragment(kind, value))
        return tokens

    def __call__(self, query : str) -> list[Fragment]:
        return self.parse(query)



    