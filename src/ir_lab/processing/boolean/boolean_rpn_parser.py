from ..base.rpn.rpn_parser import RPNParser
from ..base.fragments import *

class BooleanRPNParser(RPNParser):
    def __init__(self):
        self.operators = {
            'not': {
                "precedence" :3 ,
                "class"  : UnaryFramgent
            },
            'and': {
                "precedence" :2 ,
                "class"  : BinaryFragment
            },
            'or':{
                "precedence" :1 ,
                "class"  : BinaryFragment
            },
        }
        self.token_specification = [
        ('OP',    r'\b(?:and|or|not)\b'),
        ('TERM',  r'[^\s()]+'),
        ('SKIP',  r'[\s\t]+'),
        ]




if __name__ == "__main__":
    

    text = "information.retrieval and cookies"
    parser = BooleanRPNParser()
    print(parser(text))

    