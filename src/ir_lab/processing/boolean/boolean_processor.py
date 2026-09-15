from ..base.base_processor import BaseProcessor
from ir_lab.models.queries import Query
from ir_lab.models.documents import ScoredDocument
from .boolean_rpn_parser import BooleanRPNParser
from .boolean_retriever import BooleanRetriever
from .boolean_ast_builder import BooleanAstBuilder
from .boolean_evaluator import BooleanEvaluator
from .boolean_results_mapper import BooleanResultsMapper

from dataclasses import dataclass


@dataclass(slots=True)
class BooleanProcessor(BaseProcessor):

    parser : BooleanRPNParser
    evaluator : BooleanEvaluator
    builder : BooleanAstBuilder
    mapper : BooleanResultsMapper

    def process(self,query : Query) -> list[ScoredDocument]:
        rpn = self.parser(query.content)
        self.query_analyzer(rpn)
        ast = self.builder(rpn)
        doc_ids = self.evaluator(ast)
        results = self.mapper(doc_ids)
        return results




if __name__ == '__main__':
    from ir_lab.test.fixtures import Fixtures
    from ir_lab.analyzing.analyzers import QueryAnalyzer

    index = Fixtures.inverted_index()
    analyzer = Fixtures.analyzer()
    parser = BooleanRPNParser()
    retriever = BooleanRetriever(index)
    evaluator = BooleanEvaluator(retriever)
    builder = BooleanAstBuilder()
    mapper = BooleanResultsMapper()

    processor = BooleanProcessor(
        query_analyzer=QueryAnalyzer(analyzer),
        parser=parser,
        evaluator=evaluator,
        builder=builder,
        mapper=mapper,
    )
    query = Fixtures.query()
    print(processor([query]))
