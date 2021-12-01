from .interfaces import SignProvider
class NoneSignProvider(SignProvider):
    """A mock implementation for the none sign provider interface"""
    
    def sign(self, content: bytes) -> str:
        return content.decode("utf-8") 

    def verify(self, content: bytes, signed: bytes) -> bool:
        return content == signed