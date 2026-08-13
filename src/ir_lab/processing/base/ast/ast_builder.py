from .ast_tree import ASTTree
from .nodes import *
from ir_lab.retrieval.parsers.rpn.rpn_stack import RPNStack

class ASTBuilder:

    def __call__(self, rpn : RPNStack) -> ASTTree:
        node_stack = []

        for fragment in rpn:
            if fragment.type == "TERM":
                node_stack.append(TermNode(fragment.content))

            elif fragment.type == "OP":
                right = node_stack.pop()
                left = node_stack.pop()

                node_stack.append(
                    BinaryNode(
                        fragment.content,
                        left,
                        right,
                    )
                )

        tree = ASTTree()
        tree.stack = node_stack
        return tree
    


if __name__ == "__main__" :
    from ir_lab.test import Fixtures 
  
    
    stack = Fixtures.rpn_analyzed_stack
    builder  = ASTBuilder()
    tree = builder(stack)
    print("original stack = ",stack)
    print("built stack = ",tree.stack)

    tree.print_tree()


