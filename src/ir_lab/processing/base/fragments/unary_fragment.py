from .fragment import Fragment 
from dataclasses import dataclass


@dataclass
class UnaryFramgent(Fragment) : 
    operation : str 
    operand : Fragment