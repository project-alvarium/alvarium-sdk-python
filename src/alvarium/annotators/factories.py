from .interfaces import Annotator
from alvarium.contracts.annotation import AnnotationType
from alvarium.sign.contracts import SignInfo
from alvarium.hash.contracts import HashType
from .exceptions import AnnotatorException
from .mock import MockAnnotator
from .tpm import TpmAnnotator
from .pki import PkiAnnotator
from .source import SourceAnnotator
from .tls import TlsAnnotator

class AnnotatorFactory():

    def getAnnotator(self, kind: AnnotationType, hash: HashType, signature: SignInfo) -> Annotator:

        if kind == AnnotationType.MOCK:
            return MockAnnotator(hash=hash, signature=signature, kind=kind)
        elif kind == AnnotationType.TPM:
            return TpmAnnotator(hash=hash, sign_info=signature)
        elif kind == AnnotationType.SOURCE:
            return SourceAnnotator(hash=hash, sign_info=signature)
        elif kind == AnnotationType.TLS:
            return TlsAnnotator(hash=hash, signature=signature)
        elif kind == AnnotationType.PKI:
            return PkiAnnotator(hash=hash, sign_info=signature)
        else:
            raise AnnotatorException("Annotator type is not supported")
            
