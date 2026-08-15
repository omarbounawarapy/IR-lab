from ..base.query_processor import QueryProcessor
from ir_lab.models.queries import Query
from ir_lab.models.documents import ScoredDocument
from .boolean_rpn_parser import BooleanRPNParser
from .boolean_retriever import BooleanRetriever
from .boolean_ast_builder import BooleanAstBuilder
from .boolean_retriever import BooleanRetriever
from .boolean_evaluator import BooleanEvaluator
from .boolean_results_mapper import BooleanResultsMapper

class BooleanQueryProcessor(QueryProcessor):
    def __init__(self, analyzer, index):
        super().__init__(analyzer, index)
        self.parser = BooleanRPNParser()
        self.retriever = BooleanRetriever(index)        
        self.evaluator = BooleanEvaluator(self.retriever)
        self.builder = BooleanAstBuilder()
        self.mapper = BooleanResultsMapper()

    def process(self,query: Query) -> list[ScoredDocument]:
        rpn = self.parser(query.content)
        self.analyzer(rpn)

        ast = self.builder(rpn)
        docs = self.evaluator(ast)
        results = self.mapper(docs)
        return results
    def __call__(self,query:Query) -> list[ScoredDocument] : 
        return self.process(query)

if __name__ == '__main__': 
    from ir_lab.test.fixtures import Fixtures
    index = Fixtures.inverted_index()
    analyzer = Fixtures.analyzer()
    processor = BooleanQueryProcessor(analyzer,index)
    query = Fixtures.query()
    print(processor(query))
        