from .tokenizer import Tokenizer
from ir_lab.models.tokens import Token


class SpaceTokenizer(Tokenizer):
    def tokenize(self, text: str) -> list[Token]:
        return [
            Token(content=word, position=i)
            for i, word in enumerate(text.split())
        ]