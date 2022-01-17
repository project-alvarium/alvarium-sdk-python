from .interfaces import HashProvider
import hashlib

class SHA256Provider(HashProvider):

    def derive(self, data: bytes) -> str:
        """returns the hexadecimal md5 hash representation of the given data"""
        _m = hashlib.sha256()
        _m.update(data)
        return _m.hexdigest()