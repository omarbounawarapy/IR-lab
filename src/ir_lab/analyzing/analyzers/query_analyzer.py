from .analyzer import Analyzer
from .analyzer_builder import AnalyzerBuilder
from ir_lab.processing.base.rpn.rpn_stack import RPNStack



class QueryAnalyzer:
    def __init__(self,analyzer : Analyzer):
        self.analyzer = analyzer

    def analyze(self, rpn:RPNStack) -> None:
        for fragment in rpn : 
            if fragment.type != "OP" : 
              analysis_results = self.analyzer.analyze_content(fragment.content)
              fragment.content = analysis_results.tokens

    def __call__(self,rpn:RPNStack)->None : 
        self.analyze(rpn)

if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    builder = AnalyzerBuilder()
    query = Fixtures.rpn_stack()
    analyzer = Fixtures.analyzer()
    q_analyzer = QueryAnalyzer(analyzer)
    q_analyzer.analyze(query)
    print(query)


    