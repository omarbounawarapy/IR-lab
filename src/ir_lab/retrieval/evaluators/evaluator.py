from ..parsers.ast.nodes import BinaryNode , TermNode , UnaryNode
from abc import abstractmethod
from ..parsers.rpn.rpn_stack import RPNStack

class Evaluator:

    def __init__(self, retriever):
        self.retriever = retriever 

    def __call__(self, rpn : RPNStack):

        return self.evaluate(rpn.[-1])

    def evaluate(self, node):

        if isinstance(node, TermNode):
            return self.index.get(node.content)

        if isinstance(node, BinaryNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            return self.evaluate_binary(
                node.operator,
                left,
                right
            )
        elif isinstance(node,UnaryNode): 
            operand = self.evaluate(node.operand)

            return self.evaluate_unary(
                node.operator,
                operand
            )

        raise TypeError(f"Unsupported node: {type(node)}")


    def

    @abstractmethod
    def evaluate_binary(self, operator, left, right):
        pass 

    @abstractmethod 
    def evaluate_unary(self,operator,operand) : 
        pass 


