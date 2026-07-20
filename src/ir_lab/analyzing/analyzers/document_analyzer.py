from ir_lab.models.documents import AnalyzedDocument
from .analyzer import Analyzer

class DocumentAnalyzer:

    def __init__(self, analyzer : Analyzer ) -> AnalyzedDocument:
        self.analyzer = analyzer

    def analyze(self, document):
        analysis_results = self.analyzer.analyze(document.content)
        tokens = getattr(analysis_results,"tokens",[])

        return AnalyzedDocument(
            id=document.id,
            tokens=tokens,
            metadata=document.metadata
        )