from abc import ABC,abstractmethod

class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> Iterable[Token]:
        pass

    def __call__(self, text: str)-> Iterable[Token]:
            return self.tokenize(text)


