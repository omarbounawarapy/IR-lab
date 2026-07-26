from abc import ABC,abstractmethod
from ir_lab.models.tokens import Token


class TokenFilter(ABC):


    @abstractmethod
    def apply(self, token: Token) -> Token | None:
        pass

    def __call__(self, token: Token)-> Token | None:
        return self.apply(token)