from dataclasses import dataclass

from .ast_node import ASTNode


@dataclass
class BinaryNode(ASTNode) : 
        operator : ASTNode 
        right : ASTNode
        left : ASTNode