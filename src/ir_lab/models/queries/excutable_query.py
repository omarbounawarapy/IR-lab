from dataclasses import dataclass
from .query import Query
@dataclass
class ExecutableQuery :
    query = Query
    stack : list[str]
