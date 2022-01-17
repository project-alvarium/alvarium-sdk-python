from abc import ABC, abstractmethod
from alvarium.contracts.publish import PublishWrapper

class StreamProvider(ABC):
    """A unit that serves as an interface for a stream provider"""

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def publish(self, wrapper: PublishWrapper) -> None:
        pass