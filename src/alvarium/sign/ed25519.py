from .interfaces import SignProvider

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519


class Ed25519SignProvider(SignProvider):
    """The implementation of the Ed25519 sign provider interface"""

    def sign(self, key: bytes, content: bytes) -> str:
        key = key[:32]
        loaded_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(key)
        return bytes.hex(loaded_private_key.sign(content)) 

    def verify(self, key: bytes, content: bytes, signed: bytes) -> bool:
        loaded_public_key = ed25519.Ed25519PublicKey.from_public_bytes(key)
        try:
            loaded_public_key.verify(signed, content)
        except InvalidSignature:
            return False

        return True
