from .interfaces import HashProvider
import hashlib

class MD5Provider(HashProvider): 

    def derive(self, data: bytes) -> str:
        """returns the hexadecimal md5 hash representation of the given data"""
        _m = hashlib.md5()
        _m.update(data)
        return _m.hexdigest()