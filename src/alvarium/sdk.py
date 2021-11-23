from abc import ABC, abstractmethod

class Sdk(ABC):
    """This unit serves as an interface for the sdk."""

    @abstractmethod
    def create(self, data, properties=None) -> None:
        pass

    @abstractmethod
    def mutate(self, old_data, new_data, properties=None) -> None:
        pass

    @abstractmethod
    def transit(self, data, properties=None) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass