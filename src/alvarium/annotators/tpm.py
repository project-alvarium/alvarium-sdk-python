import socket

from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType
from alvarium.sign.contracts import SignInfo
from alvarium.utils import PropertyBag
from os import path
from .interfaces import Annotator
from .utils import derive_hash, sign_annotation

class TpmAnnotator(Annotator):

    _DIRECT_TPM_PATH = "/dev/tpm0"
    _TPM_KERNEL_MANAGED_PATH = "/dev/tpmrm0"

    def __init__(self, hash: HashType, sign_info: SignInfo) -> None:
        self.hash = hash
        self.sign_info = sign_info
        self.kind = AnnotationType.TPM
    
    def _check_tpm_exists(self, directory: str) -> bool:
        if not path.exists(path=directory):
            return False
        
        try:
            file = open(directory, "w+")
            file.close()
            return True
        except OSError as e:
            return False
    
    def execute(self, data: bytes, ctx: PropertyBag = None) -> Annotation:
        key: str = derive_hash(hash=self.hash, data=data)
        host: str = socket.gethostname()
        is_satisfied:bool = self._check_tpm_exists(self._TPM_KERNEL_MANAGED_PATH) or \
                            self._check_tpm_exists(self._DIRECT_TPM_PATH) 

        annotation = Annotation(key=key, host=host, hash=self.hash, kind=self.kind, is_satisfied=is_satisfied)

        signature: str = sign_annotation(key_info=self.sign_info.private, annotation=annotation)
        annotation.signature = signature
        return annotation