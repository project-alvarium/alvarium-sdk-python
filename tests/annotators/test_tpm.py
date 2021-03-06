import unittest
from alvarium.annotators.factories import AnnotatorFactory
from alvarium.contracts.annotation import AnnotationType
from alvarium.contracts.config import SdkInfo
from alvarium.hash.contracts import HashInfo, HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType

# implementing tests for is_satisfied in the tpm case is omitted
# as the test will not be platform agnostic
class TestTpmAnnotator(unittest.TestCase):

    def test_execute_should_return_annotation(self):
        hash = HashType.SHA256
        kind = AnnotationType.TPM
        private_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key")
        public_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/public.key")
        sign_info = SignInfo(private=private_key, public=public_key)
        sdk_info = SdkInfo(annotators=[], signature=sign_info, hash=HashInfo(type=hash), stream=[])

        annotator = AnnotatorFactory().get_annotator(kind=kind, sdk_info=sdk_info)

        test_data = b"test data"
        result = annotator.execute(data=test_data)
        self.assertEqual(kind, result.kind)
        self.assertEqual(hash, result.hash)
        self.assertIsNotNone(result.signature)
        self.assertIsNotNone(result.is_satisfied)

if __name__ == "__main__":
    unittest.main()