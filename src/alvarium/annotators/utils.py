from alvarium.annotators.contracts import Signable
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

def verify_signature(key: KeyInfo, signable: Signable) -> bool:
        """ Responsible for verifying the signature, returns true if the verification passed
            , false otherwise."""
        try:
            sign_provider = SignProviderFactory().get_provider(sign_type=key.type)
        except SignException as e:
            raise AnnotatorException("cannot get sign provider.", e)
        
        try:
            with open(key.path, 'r') as file:
                pub_key = file.read()

                try:
                    hex_pub_key = bytes.fromhex(pub_key)
                except Exception as e:
                    raise AnnotatorException("Cannot read Public Key File.",e)

                try:
                    hex_signature = bytes.fromhex(signable.signature)
                except Exception as e:
                    raise AnnotatorException("Invalid signature syntax: It is not in hex.",e)

                return sign_provider.verify(key=hex_pub_key, 
                                            content=bytes(signable.seed, 'utf-8'),
                                            signed=hex_signature)
        except OSError:
            raise AnnotatorException("Cannot read Public Key File.")