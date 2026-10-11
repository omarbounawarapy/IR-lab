from abc import ABC, abstractmethod


class Store[T](ABC):

    @abstractmethod
    def load(self) -> T:
        pass

    @abstractmethod
    def save(self, value: T) -> None:
        pass