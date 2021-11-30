from .sha256_provider import SHA256Provider
from .exceptions import HashException
from .mock import NoneHashProvider
from .contracts import HashType
from .interfaces import HashProvider

class HashProviderFactory:
    """A factory that provides a way to instaniate different types of
    Hash Providers."""

    def getProvider(self, hash_type: HashType) -> HashProvider:
        if hash_type == HashType.NONE:
            return NoneHashProvider() 
        if hash_type == HashType.SHA256:
            return SHA256Provider() 
        else:
            raise HashException(f'{hash_type} is not implemented')