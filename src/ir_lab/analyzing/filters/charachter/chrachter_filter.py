from abc import ABC,abstractmethod



class CharacterFilter(ABC):
    @abstractmethod
    def apply(self, text: str) -> str:
        pass