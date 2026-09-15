from ir_lab.analyzing.analyzers import QueryAnalyzer
from ir_lab.indexing.indexes import BaseIndex

from .boolean.boolean_processor import BooleanProcessor
from .boolean.boolean_rpn_parser import BooleanRPNParser
from .boolean.boolean_ast_builder import BooleanAstBuilder
from .boolean.boolean_retriever import BooleanRetriever
from .boolean.boolean_evaluator import BooleanEvaluator
from .boolean.boolean_results_mapper import BooleanResultsMapper


def _build_boolean(config: dict, analyzer, index: BaseIndex) -> BooleanProcessor:
    retriever = BooleanRetriever(index)
    return BooleanProcessor(
        query_analyzer=QueryAnalyzer(analyzer),
        parser=BooleanRPNParser(),
        evaluator=BooleanEvaluator(retriever),
        builder=BooleanAstBuilder(),
        mapper=BooleanResultsMapper(),
    )


RETRIEVAL_MODELS = {
    "boolean": _build_boolean,
}


class ProcessorBuilder:

    def build(self, config: dict, analyzer, index: BaseIndex):
        try:
            factory = RETRIEVAL_MODELS[config["type"]]
        except KeyError:
            raise ValueError(f"Unsupported retrieval type: {config.get('type')!r}")
        return factory(config, analyzer, index)

    def __call__(self, config: dict, analyzer, index: BaseIndex):
        return self.build(config, analyzer, index)
