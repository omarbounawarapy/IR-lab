from .ast_node import ASTNode

class BinaryNode(ASTNode) : 
    def __init__(self,op,left,right) : 
        self.operator = op 
        self.right = right
        self.left = left