@abstractclass
class QuerryTransformer(ABC):
    @abstractmethod
    def transform(self, querry: ExecutableQuerry) -> ExecutableQuerry:
        pass