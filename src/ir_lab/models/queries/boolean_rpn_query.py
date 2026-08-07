
from .executable_query import ExecutableQuery
from dataclasses import dataclass

@dataclass 
class BooleanRPNQuery(ExecutableQuery):
    stack : list[str]
    