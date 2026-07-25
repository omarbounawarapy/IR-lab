from .executable_query import ExecutableQuery
class BooleanASTQuery(ExecutableQuery):
    def __init__(self, ast: str):
        self.ast = ast