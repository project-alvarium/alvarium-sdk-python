from .interfaces import HashProvider
import hashlib

class MD5Provider(HashProvider): 
    """returns the hexadecimal md5 hash representation of the given data"""

    def derive(self, data: bytes) -> str:
        _m = hashlib.md5()
        _m.update(  data )
        return _m.hexdigest()