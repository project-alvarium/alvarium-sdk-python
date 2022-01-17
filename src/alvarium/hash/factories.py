from .sha256 import SHA256Provider
from .md5 import MD5Provider
from .exceptions import HashException
from .mock import NoneHashProvider
from .contracts import HashType
from .interfaces import HashProvider

class HashProviderFactory:
    """A factory that provides a way to instaniate different types of
    Hash Providers."""

    def get_provider(self, hash_type: HashType) -> HashProvider:
        if hash_type == HashType.NONE:
            return NoneHashProvider() 
        elif hash_type == HashType.SHA256:
            return SHA256Provider()
        elif hash_type == HashType.MD5:
            return MD5Provider()
        else:
            raise HashException(f'{hash_type} is not implemented')