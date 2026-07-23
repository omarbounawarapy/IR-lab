from .token_filter import TokenFilter 
from ir_lab.models.tokens import Token
from ir_lab.test import Fixtures

class LowerCaseTokenFilter(TokenFilter):
    def apply(self, token):
        token.content = token.content.lower()
        return token



if __name__ == "__main__" : 
    token  = Fixtures.token()
    cls = LowerCaseTokenFilter()
    print(f"{cls(token)=}")