class BooleanASTQuery(ExecutableQuerry):
    def __init__(self, ast: ASTNode):
        self.ast = ast