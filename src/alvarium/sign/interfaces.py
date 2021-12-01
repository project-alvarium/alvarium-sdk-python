from abc import ABC, abstractmethod

class SignProvider(ABC):
    """a unit that provides an interface for signing and verifying the data"""

    @abstractmethod
    def sign(self, key: bytes, content: bytes) -> str:
        """a function for signing the data"""
        pass

    @abstractmethod
    def verify(self, key: bytes, content: bytes, signed: bytes) -> str:
        """a function for verifying the data"""
        pass
