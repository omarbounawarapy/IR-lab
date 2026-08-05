from dataclasses import dataclass
from .query import Query

@dataclass 
class BooleanRPNQuery:
    query = Query
    stack : list[str]
