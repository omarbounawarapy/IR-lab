from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class Store(ABC, Generic[T]):

    @abstractmethod
    def load(self) -> T:
        pass

    @abstractmethod
    def save(self, value: T) -> None:
        pass