from information_retrival_lab.src.core.models.excutable_querries.executable_querry import ExecutableQuerry


@abstractclass
class QuerryTransformer(ABC):
    @abstractmethod
    def transform(self, querry: ExecutableQuerry) -> ExecutableQuerry:
        pass