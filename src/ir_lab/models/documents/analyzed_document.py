from .document import Document
from ir_lab.models.tokens import Token

class AnalyzedDocument:
    def __init__(self,document : Document, tokens : list[Token]):
        self.document = document
        self.tokens = tokens

    def __str__(self):
        return f"{self.tokens=}"

    
    def term_set(self):
        return set([token.content for token in self.tokens])