class CharacterFilter(ABC):
    @abstractmethod
    def apply(self, text: str) -> str:
        pass


class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> Iterable[Token]:
        pass


class TokenFilter(ABC):
    @abstractmethod
    def apply(self, tokens: Iterable[Token]) -> Iterable[Token]:
        pass