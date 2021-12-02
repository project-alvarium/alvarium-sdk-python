from .interfaces import SignProvider
from .contracts import SignType
from .exceptions import SignException
from .mock import NoneSignProvider
from .ed25519_sign_provider import Ed25519ignProvider


class SignProviderFactory:
    """A factory that provides a way to instaniate different types of
    Sign Providers."""

    def getProvider(self, sign_type: SignType) -> SignProvider:
        """A function returns sign provider based on what sign type it gets"""

        if sign_type == SignType.NONE:
            return NoneSignProvider()
        if sign_type == SignType.ED25519:
            return Ed25519ignProvider()
        else:
            raise SignException(f'{sign_type} is not implemented yet')
