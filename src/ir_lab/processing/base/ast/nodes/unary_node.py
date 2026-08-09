from .ast_node import ASTNode
from dataclasses import dataclass


@dataclass
class UnaryNode(ASTNode): 
    operand : ASTNode