from .document import Document
from models import Token

class AnalyzedDocument:
    def __init__(self,document : Document, tokens : list[Token]):
        self.document = document
        self.tokens = tokens