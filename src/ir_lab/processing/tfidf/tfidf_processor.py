from dataclasses import dataclass

from ..base.base_processor import BaseProcessor
from ir_lab.models.queries import Query
from ir_lab.models.documents import ScoredDocument
from .tfidf_retriever import TFIDFRetriever
from .tfidf_results_mapper import TFIDFResultsMapper


@dataclass(slots=True)
class TFIDFProcessor(BaseProcessor):
    """A free-text, ranked retrieval model -- proves BaseProcessor's
    contract generalizes beyond boolean's query-language pipeline
    (RPN -> AST -> evaluator): this model needs none of that, only the
    analyzer already carried by query_analyzer."""

    retriever: TFIDFRetriever
    mapper: TFIDFResultsMapper
    top_k: int | None = None

    def process(self, query: Query) -> list[ScoredDocument]:
        tokens = self.query_analyzer.analyzer.analyze_content(query.content).tokens
        scored_pairs = self.retriever.score([token.content for token in tokens])
        if self.top_k is not None:
            scored_pairs = scored_pairs[: self.top_k]
        return self.mapper(scored_pairs)


if __name__ == "__main__":
    from ir_lab.test.fixtures import Fixtures
    from ir_lab.analyzing.analyzers import QueryAnalyzer
    from ir_lab.indexing.indexers.inverted_indexer import InvertedIndexer

    analyzer = Fixtures.analyzer()
    index = InvertedIndexer()(Fixtures.analyzed_documents())
    processor = TFIDFProcessor(
        query_analyzer=QueryAnalyzer(analyzer),
        retriever=TFIDFRetriever(index),
        mapper=TFIDFResultsMapper(),
    )
    print(processor([Fixtures.query()]))
