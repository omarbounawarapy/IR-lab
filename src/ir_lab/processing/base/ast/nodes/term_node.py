from .ast_node import ASTNode
from dataclasses import dataclass
from ir_lab.models.tokens import Token


@dataclass
class TermNode(ASTNode) : 
    content : list[Token]