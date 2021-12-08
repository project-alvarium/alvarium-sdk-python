from alvarium.contracts.annotation import AnnotationType
from alvarium.sign.contracts import SignInfo
from alvarium.hash.contracts import HashType
from .exceptions import AnnotatorException
from .mock import MockAnnotator

class AnnotatorFactory():

    def getAnnotator(self, kind: AnnotationType, hash: HashType, signature: SignInfo):

        if kind == AnnotationType.MOCK:
            return MockAnnotator(hash=hash, signature=signature, kind=kind)
        else:
            raise AnnotatorException("Annotator type is not supported")
            
