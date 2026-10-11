from dataclasses import dataclass

from ir_lab.models.tokens import Token

from .ast_node import ASTNode


@dataclass
class TermNode(ASTNode) : 
    content : list[Token]