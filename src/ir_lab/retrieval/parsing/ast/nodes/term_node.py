from .ast_node import ASTNode

class TermNode(ASTNode) : 
    def __init__(self, content) : 
        self.content = content