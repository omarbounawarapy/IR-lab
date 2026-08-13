from .rpn_parser import RPNParser
class BooleanRPNParser(RPNParser):
    def __init__(self):
        self.operators = {
            'and': 1,
            'or': 2,
            'not': 3
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

    