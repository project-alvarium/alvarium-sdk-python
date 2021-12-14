from abc import ABC, abstractmethod
from alvarium.utils import PropertyBag

class Sdk(ABC):
    """This unit serves as an interface for the sdk."""

    @abstractmethod
    def create(self, data: bytes, properties: PropertyBag = None) -> None:
        pass

    @abstractmethod
    def mutate(self, old_data: bytes, new_data: bytes, properties: PropertyBag = None) -> None:
        pass

    @abstractmethod
    def transit(self, data: bytes, properties: PropertyBag = None) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass