from .interfaces import Annotator
from alvarium.annotators.tls_anotator import TlsAnotator
from alvarium.contracts.annotation import AnnotationType
from alvarium.sign.contracts import SignInfo
from alvarium.hash.contracts import HashType
from .exceptions import AnnotatorException
from .mock import MockAnnotator
from .tpm import TpmAnnotator
from .source import SourceAnnotator

class AnnotatorFactory():

    def getAnnotator(self, kind: AnnotationType, hash: HashType, signature: SignInfo) -> Annotator:

        if kind == AnnotationType.MOCK:
            return MockAnnotator(hash=hash, signature=signature, kind=kind)
        elif kind == AnnotationType.TPM:
            return TpmAnnotator(hash=hash, sign_info=signature)
        elif kind == AnnotationType.SOURCE:
            return SourceAnnotator(hash=hash, sign_info=signature)
        elif kind == AnnotationType.TLS:
            return TlsAnotator(hash=hash, signature=signature)
        else:
            raise AnnotatorException("Annotator type is not supported")
            
