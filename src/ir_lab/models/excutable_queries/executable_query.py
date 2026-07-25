from abc import ABC, abstractmethod

class ExecutableQuery(ABC):
    @abstractmethod
    def __init__(self,data:any):
        self.data = data