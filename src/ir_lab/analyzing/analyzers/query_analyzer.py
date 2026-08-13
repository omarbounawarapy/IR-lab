from .analyzer import Analyzer
from ir_lab.retrieval.parsers.rpn.rpn_stack import RPNStack



class QueryAnalyzer:

    def __init__(self, analyzer : Analyzer):
        self.analyzer = analyzer

    def analyze(self, rpn:RPNStack) -> None:
        for fragment in rpn : 
            if fragment.type != "OP" : 
              analysis_results = self.analyzer.analyze(fragment.content)
              fragment.content = analysis_results.tokens

    def __call__(self,rpn:RPNStack)->None : 
        self.analyze(rpn)

if __name__ == "__main__" : 
    from ir_lab.test import Fixtures
    query = Fixtures.rpn_stack()
    analyzer = Fixtures.analyzer()
    q_analyzer = QueryAnalyzer(analyzer=analyzer)
    q_analyzer.analyze(query)
    print(query)


    