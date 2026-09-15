from ir_lab.analyzing.analyzers import QueryAnalyzer
from ir_lab.indexing.indexes import BaseIndex
from ir_lab.errors import ConfigError

from .boolean.boolean_processor import BooleanProcessor
from .boolean.boolean_rpn_parser import BooleanRPNParser
from .boolean.boolean_ast_builder import BooleanAstBuilder
from .boolean.boolean_retriever import BooleanRetriever
from .boolean.boolean_evaluator import BooleanEvaluator
from .boolean.boolean_results_mapper import BooleanResultsMapper

from .tfidf.tfidf_processor import TFIDFProcessor
from .tfidf.tfidf_retriever import TFIDFRetriever
from .tfidf.tfidf_results_mapper import TFIDFResultsMapper


def _build_boolean(config: dict, analyzer, index: BaseIndex) -> BooleanProcessor:
    retriever = BooleanRetriever(index)
    return BooleanProcessor(
        query_analyzer=QueryAnalyzer(analyzer),
        parser=BooleanRPNParser(),
        evaluator=BooleanEvaluator(retriever),
        builder=BooleanAstBuilder(),
        mapper=BooleanResultsMapper(),
    )


def _build_tfidf(config: dict, analyzer, index: BaseIndex) -> TFIDFProcessor:
    return TFIDFProcessor(
        query_analyzer=QueryAnalyzer(analyzer),
        retriever=TFIDFRetriever(index),
        mapper=TFIDFResultsMapper(),
    )


RETRIEVAL_MODELS = {
    "boolean": _build_boolean,
    "tfidf": _build_tfidf,
}


class ProcessorBuilder:

    def build(self, config: dict, analyzer, index: BaseIndex):
        try:
            retrieval_type = config["type"]
        except KeyError:
            raise ConfigError(f"retrieval config is missing a 'type' field: {config!r}")

        try:
            factory = RETRIEVAL_MODELS[retrieval_type]
        except KeyError:
            raise ConfigError(
                f"unknown retrieval type {retrieval_type!r}; "
                f"expected one of {sorted(RETRIEVAL_MODELS)}"
            )
        return factory(config, analyzer, index)

    def __call__(self, config: dict, analyzer, index: BaseIndex):
        return self.build(config, analyzer, index)
