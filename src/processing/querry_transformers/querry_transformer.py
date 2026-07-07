@abstractclass
class QuerryTransformer(ABC):
    @abstractmethod
    def transform(self, querry: Querry) -> ExecutableQuerry:
        pass