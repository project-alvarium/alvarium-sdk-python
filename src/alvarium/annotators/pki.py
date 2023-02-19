import socket

from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType
from alvarium.sign.contracts import SignInfo
from alvarium.utils import PropertyBag
from .contracts import Signable
from .utils import derive_hash, sign_annotation, verify_signature
from .interfaces import Annotator

class PkiAnnotator(Annotator):

    def __init__(self, hash: HashType, sign_info: SignInfo) -> None:
        self.hash = hash
        self.sign_info = sign_info
        self.kind = AnnotationType.PKI

    def execute(self, data: bytes, ctx: PropertyBag = None) -> Annotation:
        key = derive_hash(hash=self.hash, data=data)
        host: str = socket.gethostname()

        # create Signable object
        signable = Signable.from_json(data.decode('utf-8'))
        is_satisfied: bool = verify_signature(key=self.sign_info.public, signable=signable) 

        annotation = Annotation(key=key, host=host, hash=self.hash, kind=self.kind, is_satisfied=is_satisfied)
        
        signature: str = sign_annotation(key_info=self.sign_info.private, annotation=annotation)
        annotation.signature = signature
        return annotation
