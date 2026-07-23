from abc import ABC,abstractmethod



class CharFilter(ABC):
    @abstractmethod
    def apply(self, text: str) -> str:
        pass

    def __call__(self, text: str)-> str:
        return self.apply(text)