from .ast_tree import ASTTree
from .nodes import *
from ir_lab.retrieval.parsing import RPNStack
from ..rpn.boolean_rpn_parser import BooleanRPNParser
from ir_lab.analyzing.analyzers import QueryAnalyzer

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
  
    parser = BooleanRPNParser()
    query = "information or retrieval"
    stack = parser(query)
    analyzer = Fixtures.analyzer()
    q_analyzer = QueryAnalyzer(analyzer)
    builder  = ASTBuilder()
    q_analyzer(stack)
    tree = builder(stack)
    print("original stack = ",stack)
    print("built stack = ",tree.stack)

    tree.print_tree()


