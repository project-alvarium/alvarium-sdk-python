from alvarium.contracts.config import SdkInfo
from .interfaces import Annotator
from alvarium.contracts.annotation import AnnotationType
from .exceptions import AnnotatorException
from .mock import MockAnnotator
from .tpm import TpmAnnotator
from .pki import PkiAnnotator
from .source import SourceAnnotator
from .tls import TlsAnnotator
from .pki_http import HttpPkiAnnotator

class AnnotatorFactory():
    """A factory that provides multiple implementations of the Annotator interface"""

    def get_annotator(self, kind: AnnotationType, sdk_info: SdkInfo) -> Annotator:

        if kind == AnnotationType.MOCK:
            return MockAnnotator(hash=sdk_info.hash.type, signature=sdk_info.signature, kind=kind)
        elif kind == AnnotationType.TPM:
            return TpmAnnotator(hash=sdk_info.hash.type, sign_info=sdk_info.signature)
        elif kind == AnnotationType.SOURCE:
            return SourceAnnotator(hash=sdk_info.hash.type, sign_info=sdk_info.signature)
        elif kind == AnnotationType.TLS:
            return TlsAnnotator(hash=sdk_info.hash.type, signature=sdk_info.signature)
        elif kind == AnnotationType.PKI:
            return PkiAnnotator(hash=sdk_info.hash.type, sign_info=sdk_info.signature)
        elif kind == AnnotationType.PKI_HTTP:
            return HttpPkiAnnotator(hash=sdk_info.hash.type, sign_info=sdk_info.signature)
        else:
            raise AnnotatorException("Annotator type is not supported")
