from .ast_tree import ASTTree
from .nodes import *
from ir_lab.retrieval.parsing import Fragment
from ir_lab.models.tokens import Token

class ASTBuilder:

    def __call__(self, rpn: list[Fragment]) -> ASTTree:
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
    stack = [Fragment(type='TERM', content=[Token(content='information', position=0, start_offset=None, end_offset=None, payload={})]), 
             Fragment(type='TERM', content=[Token(content='retrieval', position=0, start_offset=None, end_offset=None, payload={})]),
             Fragment(type='OP', content='and')]
    
    builder  = ASTBuilder()
    tree = builder(stack)
    print("original stack = ",stack)
    print("built stack = ",tree.stack)

    tree.print_tree()


