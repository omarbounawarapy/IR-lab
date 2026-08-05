from .analyzer import Analyzer
from ir_lab.models.queries import AnalyzedQuery,Query


class QueryAnalyzer:

    def __init__(self, analyzer : Analyzer):
        self.analyzer = analyzer

    def analyze(self, query:Query) -> AnalyzedQuery:
        analysis_results = self.analyzer.analyze(query.content)
        tokens = getattr(analysis_results,"tokens",[])

        return AnalyzedQuery(
            query=query,
            tokens=tokens
        )

if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    from .analyzer_builder import AnalyzerBuilder
    config = Fixtures.analyzer_config()
    query = Fixtures.query()
    builder = AnalyzerBuilder()
    analyzer = builder.build(config)
    doc_analyzer = QueryAnalyzer(analyzer=analyzer)
    analyzed_query = doc_analyzer.analyze(query)
    for token in analyzed_query.tokens:
        print(f"{token=}")

    