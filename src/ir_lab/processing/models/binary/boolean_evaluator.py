from .evaluator import Evaluator
from ..retrievers.binary.binary_retriever import BinaryRetriever


class BooleanEvaluator(Evaluator) : 

        def __init__(self, retriever : BinaryRetriever):
             self.retriever = retriever             
             self.operations = {
                 "and": self.retriever.intersect,
                 "or": self.retriever.union
             }


        def evaluate_binary(self, operator, left, right):
            try:
                 operation = self.operations[operator]
            except KeyError:
                raise ValueError(f"Unknown operator: {operator}")

            return operation(left, right)


if __name__ == "__main__" : 
     from ir_lab.test import Fixtures 
     from ..parsers.ast.ast_builder import ASTBuilder

     builder = ASTBuilder()
     index = Fixtures.inverted_index()
     retriever = BinaryRetriever(index)
     evaluator = BooleanEvaluator(retriever)
     analyzed_rpn  = Fixtures.rpn_analyzed_stack()
     ast = builder(analyzed_rpn)
     results = evaluator(ast)
     print(results)





