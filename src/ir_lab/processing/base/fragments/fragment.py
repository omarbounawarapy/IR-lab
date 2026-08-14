from dataclasses import dataclass
from ir_lab.models.tokens import Token

@dataclass
class Fragment : 
    content  : list[str | Token]