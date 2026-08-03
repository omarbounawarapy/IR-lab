from dataclasses import dataclass
from ir_lab.models.tokens import Token

@dataclass
class AnalysisResult:
    tokens: list[Token]
