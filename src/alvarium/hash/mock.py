from .interfaces import HashProvider

class NoneHashProvider(HashProvider):
    """A mock implementation for the HashProvider interface"""

    def derive(self, data: bytes) -> str:
        return data.decode("utf-8") 