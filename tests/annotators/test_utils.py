import unittest

from alvarium.annotators.utils import derive_hash, sign_annotation
from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType
from alvarium.sign.contracts import KeyInfo, SignType
from alvarium.sign.factories import SignProviderFactory
from alvarium.sign.interfaces import SignProvider

class TestUtils(unittest.TestCase):

    def test_derive_hash_should_return_the_right_hash(self):
        data = "this is a test"
        expected = "2e99758548972a8e8822ad47fa1017ff72f06f3ff6a016851f45c398732bc50c" #ground truth
        result: str = derive_hash(hash=HashType.SHA256, data=bytes(data, 'utf-8'))

        self.assertEqual(expected, result)
    
    def test_sign_annotation_should_return_signature(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider = factory.getProvider(SignType.ED25519)
        
        private_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key")
        annotation = Annotation(key="key", hash="hash", host="host", kind=AnnotationType.MOCK, 
                                is_satisfied=True)

        result = sign_annotation(key_info=private_key, annotation=annotation)
        
        with open(f"./tests/sign/keys/public.key", "r") as file:
            public_key_hex = file.read()
            public_key_bytes = bytes.fromhex(public_key_hex)
        
        self.assertTrue(sign_provider.verify(key=public_key_bytes,content=bytes(annotation.to_json(), 'utf-8'),
                                            signed=bytes.fromhex(result)))


if __name__ == "__main__":
    unittest.main()