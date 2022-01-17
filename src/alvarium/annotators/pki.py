import socket

from alvarium.sign.exceptions import SignException
from alvarium.sign.factories import SignProviderFactory
from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType
from alvarium.sign.contracts import KeyInfo, SignInfo
from alvarium.utils import PropertyBag
from .contracts import Signable
from .utils import derive_hash, sign_annotation
from .interfaces import Annotator
from .exceptions import AnnotatorException

class PkiAnnotator(Annotator):

    def __init__(self, hash: HashType, sign_info: SignInfo) -> None:
        self.hash = hash
        self.sign_info = sign_info
        self.kind = AnnotationType.PKI
    
    def _verify_signature(self, key: KeyInfo, signable: Signable) -> bool:
        """ Responsible for verifying the signature, returns true if the verification passed
            , false otherwise."""
        try:
            sign_provider = SignProviderFactory().get_provider(sign_type=key.type)
        except SignException as e:
            raise AnnotatorException("cannot get sign provider.", e)
        
        with open(key.path, 'r') as file:
            pub_key = file.read()
            return sign_provider.verify(key=bytes.fromhex(pub_key), 
                                        content=bytes(signable.seed, 'utf-8'),
                                        signed=bytes.fromhex(signable.signature))


    def execute(self, data: bytes, ctx: PropertyBag = None) -> Annotation:
        key = derive_hash(hash=self.hash, data=data)
        host: str = socket.gethostname()

        # create Signable object
        signable = Signable.from_json(data.decode('utf-8'))
        is_satisfied: bool = self._verify_signature(key=self.sign_info.public, signable=signable) 

        annotation = Annotation(key=key, host=host, hash=self.hash, kind=self.kind, is_satisfied=is_satisfied)
        
        signature: str = sign_annotation(key_info=self.sign_info.private, annotation=annotation)
        annotation.signature = signature
        return annotation