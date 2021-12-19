import socket
import ssl

from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.exceptions import HashException
from alvarium.hash.contracts import HashType
from alvarium.sign.contracts import SignInfo
from alvarium.utils import PropertyBag
from .utils import derive_hash, sign_annotation
from .interfaces import Annotator
from .exceptions import AnnotatorException


class TlsAnnotator(Annotator):

    hash: HashType
    signature: SignInfo
    kind: AnnotationType

    def __init__(self, hash: HashType, signature: SignInfo):
        self.hash = hash
        self.signature = signature
        self.kind = AnnotationType.TLS
    
    def execute(self, ctx: PropertyBag, data: bytes) -> Annotation:
        try:
            key = derive_hash(self.hash, data)
            is_satisfied = False
            
            context = ctx.get_property(str(AnnotationType.TLS))
            if context != None:
                # If none is returned then there is no error in handshake so tls is satisfied
                if  type(context) == ssl.SSLSocket:
                    try:
                        if context.do_handshake(block=True) == None:
                            is_satisfied = True
                    except:
                        pass

            annotation = Annotation(key= key, hash= self.hash, host= socket.gethostname(), kind= self.kind, is_satisfied= is_satisfied)
            annotation_signture = sign_annotation(self.signature.private, annotation)
            annotation.signature = str(annotation_signture)
            return annotation

        except HashException as e:
            raise AnnotatorException("failed to hash data", e)
        
        except socket.herror as e:
            raise AnnotatorException("could not get hostname", e)