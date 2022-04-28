from .interfaces import SignProvider
from .contracts import SignType
from .exceptions import SignException
from .mock import NoneSignProvider
from .ed25519 import Ed25519SignProvider


class SignProviderFactory:
    """A factory that provides a way to instaniate different types of
    Sign Providers."""

    def get_provider(self, sign_type: SignType) -> SignProvider:
        """A function returns sign provider based on what sign type it gets"""

        if sign_type == SignType.NONE:
            return NoneSignProvider()
        if sign_type == SignType.ED25519:
            return Ed25519SignProvider()
        else:
            raise SignException(f'{sign_type} is not implemented yet')
