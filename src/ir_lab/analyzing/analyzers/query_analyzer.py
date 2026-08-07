from .analyzer import Analyzer
from ir_lab.models.queries import AnalyzedQuery,Query
from ir_lab.models.tokens import Token
from ir_lab.retrieval.parsing import Fragment



class QueryAnalyzer:

    def __init__(self, analyzer : Analyzer):
        self.analyzer = analyzer

    def analyze(self, rpnquery:list[Fragment]):
        for fragment in rpnquery : 
            if fragment.type != "OP" : 
              analysis_results = self.analyzer.analyze(fragment.content)
              fragment.content = analysis_results.tokens

if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    from .analyzer_builder import AnalyzerBuilder
    config = Fixtures.analyzer_config()
    query = [Fragment(type='TERM', content='information.retrieval'), Fragment(type='TERM', content='cookies'), Fragment(type='OP', content='and')]
    builder = AnalyzerBuilder()
    analyzer = builder.build(config)
    doc_analyzer = QueryAnalyzer(analyzer=analyzer)
    doc_analyzer.analyze(query)
    for fragment in query: 
        print(fragment)


    