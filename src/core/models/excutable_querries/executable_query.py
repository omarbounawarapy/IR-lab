@abstractclass
class ExecutableQuery(ABC):
    @abstractmethod
    def __init__(self,data:any):
        self.data = data