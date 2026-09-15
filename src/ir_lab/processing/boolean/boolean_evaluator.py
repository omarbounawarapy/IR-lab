from .boolean_retriever import BooleanRetriever
from ..base.base_evaluator import BaseEvaluator
from ir_lab.errors import UnsupportedFeatureError

class BooleanEvaluator(BaseEvaluator) :

        def __init__(self, retriever : BooleanRetriever):
             super().__init__(retriever)
             self.binary_operations = {
                 "and": self.retriever.intersect,
                 "or": self.retriever.union,
             }
             self.unary_operations = {
                 "not": self.retriever.complement,
             }

        def evaluate_term(self, tokens):
            # A term made entirely of characters the analyzer discards (e.g. a
            # lone punctuation mark once punctuation filtering applies) analyzes
            # to zero tokens. Same convention as an unknown vocabulary term
            # (InvertedIndex.get_postings): matches no documents, not a crash.
            if not tokens:
                return []
            term = tokens[0].content
            return self.retriever.term_documents(term)

        def evaluate_binary(self, operator, left, right):
            try:
                 operation = self.binary_operations[operator]
            except KeyError:
                raise UnsupportedFeatureError(
                    f"boolean retrieval does not support the binary operator {operator!r} yet"
                )

            return operation(left, right)

        def evaluate_unary(self, operator, operand):
            try:
                operation = self.unary_operations[operator]
            except KeyError:
                raise UnsupportedFeatureError(
                    f"boolean retrieval does not support the unary operator {operator!r} yet"
                )

            return operation(operand)


if __name__ == "__main__" :
     from ir_lab.test import Fixtures
     from ..base.ast.ast_builder import ASTBuilder

     builder = ASTBuilder()
     index = Fixtures.inverted_index()
     retriever = BooleanRetriever(index)
     evaluator = BooleanEvaluator(retriever)
     analyzed_rpn  = Fixtures.rpn_analyzed_stack()
     ast = builder(analyzed_rpn)
     results = evaluator(ast)
     print(results)
