from .interfaces import HashProvider
import hashlib

class SHA256Provider(HashProvider):
    """returns the hexadecimal sha256 hash representation of the given data"""

    def derive(self, data: bytes) -> str:
        _m = hashlib.sha256()
        _m.update(  data )
        return _m.hexdigest()
