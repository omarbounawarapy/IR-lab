from .analyzer import Analyzer
from ir_lab.models.queries import AnalyzedQuery


class QueryAnalyzer:

    def __init__(self, analyzer : Analyzer) -> AnalyzedQuery:
        self.analyzer = analyzer

    def analyze(self, query):
        return AnalyzedQuery(
            tokens=self.analyzer.analyze(query.text)
        )