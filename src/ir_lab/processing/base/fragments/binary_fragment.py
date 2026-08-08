from .fragment import Fragment
from dataclasses import dataclass


@dataclass
class BinaryFragment(Fragment):
    operation : str 
    left : Fragment
    right : Fragment