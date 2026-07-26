from .token_filter import TokenFilter 
from ir_lab.models.tokens import Token

class LowerCaseTokenFilter(TokenFilter):
    def apply(self, token):
        token.content = token.content.lower()
        return token



if __name__ == "__main__" : 
    text = "IRLAB"
    token  = Token(content=text)
    cls = LowerCaseTokenFilter()
    token = cls(token)
    print(token)
