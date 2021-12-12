import socket

from .interfaces import Annotator
from .utils import derive_hash, sign_annotation
from alvarium.hash.contracts import HashType
from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.sign.contracts import SignInfo
from alvarium.utils import PropertyBag

class SourceAnnotator(Annotator):
    
    def __init__(self, hash: HashType, sign_info: SignInfo) -> None:
        self.hash = hash
        self.kind = AnnotationType.SOURCE
        self.sign_info = sign_info
    
    def execute(self, data: bytes, ctx: PropertyBag = None) -> Annotation:
        key: str = derive_hash(hash=self.hash, data=data)
        host: str = socket.gethostname()

        annotation = Annotation(key=key, hash=self.hash, host=host, kind=self.kind, is_satisfied=True)

        signature: str = sign_annotation(key_info=self.sign_info.private, annotation=annotation)
        annotation.signature = signature
        return annotation
