from dataclasses import dataclass
from .query import Query
@dataclass
class ExcutableQuery :
    query = Query
    stack : list[str]
