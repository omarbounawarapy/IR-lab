from ir_lab.models.tokens import Token

from .document import Document


class AnalyzedDocument:
    def __init__(self,document : Document, tokens : list[Token]):
        self.document = document
        self.tokens = tokens

    def __str__(self):
        return f"{self.tokens=}"

    
    def term_set(self):
        return {token.content for token in self.tokens}