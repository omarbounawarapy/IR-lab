from dataclasses import dataclass
from ir_lab.models.tokens import Token

@dataclass
class Fragment : 
    type : str 
    content  : list[str | Token]