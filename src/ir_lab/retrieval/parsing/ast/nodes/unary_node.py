from .ast_node import ASTNode

class UnaryNode(ASTNode): 
    def __init__(self, operand) :
        self.operand = operand