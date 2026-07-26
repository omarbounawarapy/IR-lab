from .tokenizer import Tokenizer
from ir_lab.models.tokens import Token


class SpaceTokenizer(Tokenizer):
    def tokenize(self, text: str) -> list[Token]:
        return [
            Token(content=word, position=i)
            for i, word in enumerate(text.split())
        ]



if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    text = Fixtures.text()
    cls = SpaceTokenizer()
    for token in cls(text) : 
        print(f'{token=}')