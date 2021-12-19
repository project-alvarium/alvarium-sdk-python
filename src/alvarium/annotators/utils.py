from alvarium.hash.contracts import HashType
from alvarium.hash.exceptions import HashException
from alvarium.hash.factories import HashProviderFactory
from alvarium.sign.contracts import KeyInfo
from alvarium.sign.factories import SignProviderFactory
from alvarium.sign.exceptions import SignException
from alvarium.contracts.annotation import Annotation
from .exceptions import AnnotatorException


def derive_hash(hash: HashType, data: bytes) -> str:
    """A helper to ease the hashing of incoming data."""
    try:
        hash_provider = HashProviderFactory().get_provider(hash_type=hash)
        return hash_provider.derive(data=data)
    except HashException as e:
        raise AnnotatorException("cannot hash data.", e)

def sign_annotation(key_info: KeyInfo, annotation: Annotation) -> str:
    """A helper to ease the signing process of an annotation"""
    try:
        sign_provider = SignProviderFactory().get_provider(sign_type=key_info.type)
        with open(key_info.path, "r") as file:
            key = file.read()
            return sign_provider.sign(key=bytes.fromhex(key), content=bytes(annotation.to_json(), 'utf-8'))
    except SignException as e:
        raise AnnotatorException("cannot sign annotation.", e) 
    except OSError as e:
        raise AnnotatorException("cannot open key file.", e)
