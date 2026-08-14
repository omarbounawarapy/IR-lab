from .ast_node import ASTNode
from dataclasses import dataclass


@dataclass
class BinaryNode(ASTNode) : 
        operator : ASTNode 
        right : ASTNode
        left : ASTNode