from abc import ABC, abstractmethod

class HashProvider(ABC):
    """a unit that provides an interface for hashing the incoming data"""

    @abstractmethod
    def derive(self, data: bytes) -> str:
        """returns the hash hex string representation of the input data"""
        pass