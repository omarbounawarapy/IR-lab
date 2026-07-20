from abc import ABC,abstractmethod



class TokenFilter(ABC):
    @abstractmethod
    def apply(self, tokens: Iterable[Token]) -> Iterable[Token]:
        pass