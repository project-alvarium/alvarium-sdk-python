import socket

from alvarium.annotators.handler.contracts import HttpConstants
from alvarium.annotators.handler.exceptions import ParserException

from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, KeyInfo, SignType
from alvarium.utils import PropertyBag
from .contracts import Signable
from .utils import derive_hash, sign_annotation, verify_signature
from .interfaces import Annotator
from .exceptions import AnnotatorException
from alvarium.annotators.handler.utils import parseSignature

class HttpPkiAnnotator(Annotator):
    def __init__(self, hash: HashType, sign_info: SignInfo) -> None:
        self.hash = hash
        self.sign_info = sign_info
        self.kind = AnnotationType.PKI_HTTP

    def execute(self, data: bytes, ctx: PropertyBag = None) -> Annotation:
        key = derive_hash(hash=self.hash, data=data)
        host: str = socket.gethostname()

        # Call parser on request
        req = ctx.get_property(key=HttpConstants().http_request_key)

        try:
            parsed_data = parseSignature(r=req)
        except ParserException as e:
            raise AnnotatorException("Cannot parse the HTTP request.", e)

        signable = Signable(seed=parsed_data.seed, signature=parsed_data.signature)

        try:
            signType = SignType(parsed_data.algorithm)
        except Exception as e:
            raise AnnotatorException("Invalid key type specified" + str(parsed_data.algorithm),e)

        k = KeyInfo(signType, parsed_data.keyid)

        try:
            is_satisfied = verify_signature(key=k, signable=signable)
        except Exception as e:
            raise AnnotatorException(str(e),e)
        
        annotation = Annotation(key=key, host=host, hash=self.hash, kind=self.kind, is_satisfied=is_satisfied)

        signature: str = sign_annotation(key_info=self.sign_info.private, annotation=annotation)
        annotation.signature = signature
        return annotation
