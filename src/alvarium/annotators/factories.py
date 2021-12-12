from .interfaces import Annotator
from alvarium.contracts.annotation import AnnotationType
from alvarium.sign.contracts import SignInfo
from alvarium.hash.contracts import HashType
from .exceptions import AnnotatorException
from .mock import MockAnnotator
from .tpm import TpmAnnotator

class AnnotatorFactory():

    def getAnnotator(self, kind: AnnotationType, hash: HashType, signature: SignInfo) -> Annotator:

        if kind == AnnotationType.MOCK:
            return MockAnnotator(hash=hash, signature=signature, kind=kind)
        elif kind == AnnotationType.TPM:
            return TpmAnnotator(hash=hash, sign_info=signature)
        else:
            raise AnnotatorException("Annotator type is not supported")
            
