from ..parsers.ast.nodes import BinaryNode , TermNode , UnaryNode
from abc import abstractmethod

class Evaluator:

    def __init__(self, retriever):
        self.retriever = retriever 

    def __call__(self,tree):

        return self.evaluate(tree.root())

    def evaluate(self, node):

        if isinstance(node, TermNode):
            return node.content
        

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



    @abstractmethod
    def evaluate_binary(self, operator, left, right):
        pass 

    @abstractmethod 
    def evaluate_unary(self,operator,operand) : 
        pass 


