from dataclasses import dataclass

from .ast_node import ASTNode


@dataclass
class UnaryNode(ASTNode):
    operator : str
    operand : ASTNode