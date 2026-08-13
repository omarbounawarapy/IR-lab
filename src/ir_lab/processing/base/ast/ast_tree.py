from .nodes import *

class ASTTree:
    def __init__(self):
        self.stack = []

    def add_node(self,node: ASTNode) : 
        self.stack.append(node)


    def print_tree(self):
        self.print_node(self.stack[-1])

    def root(self) : 
        return self.stack[-1]

    @staticmethod
    def print_node(node, prefix="", is_last=True):
        connector = "└── " if is_last else "├── "
        print(prefix + connector, end="")
    
        if isinstance(node, BinaryNode):
            print(node.operator)
    
            child_prefix = prefix + ("    " if is_last else "│   ")
            ASTTree.print_node(node.left, child_prefix, False)
            ASTTree.print_node(node.right, child_prefix, True)
    
        elif isinstance(node, TermNode):
            terms = " ".join(token.content for token in node.content)
            print(f'"{terms}"')
    
        else:
            print(node)