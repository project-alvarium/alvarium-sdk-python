import socket

from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType
from alvarium.hash.factories import HashProviderFactory
from alvarium.hash.exceptions import HashException
from alvarium.sign.contracts import SignInfo
from alvarium.utils import PropertyBag
from .interfaces import Annotator
from .exceptions import AnnotatorException

class MockAnnotator(Annotator):
    """a mock annotator to be used in unit tests"""

    hash: HashType
    signature: SignInfo
    kind: AnnotationType

    def __init__(self, hash: HashType, signature: SignInfo, kind: AnnotationType):
        self.hash = hash
        self.signature = signature
        self.kind = kind

    def execute(self, data: bytes, ctx: PropertyBag = None) -> Annotation:
        hashFactory = HashProviderFactory()

        try:
            key = hashFactory.getProvider(self.hash).derive(data)
            host = socket.gethostname()
            sig = self.signature.public.type.__str__()

            annotation = Annotation(key, self.hash, host, self.kind, sig, True)
            return annotation

        except HashException as e:
            raise AnnotatorException("failed to hash data", e)
        
        except socket.herror as e:
            raise AnnotatorException("could not get hostname", e)


        

