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







