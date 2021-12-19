import unittest
from alvarium.annotators.factories import AnnotatorFactory
from alvarium.contracts.annotation import AnnotationType
from alvarium.contracts.config import SdkInfo
from alvarium.hash.contracts import HashInfo, HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType

class SourceAnnotatorTest(unittest.TestCase):

    def test_execute_should_return_annotation(self):
        hash = HashType.SHA256
        kind = AnnotationType.SOURCE
        private_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key")
        public_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/public.key")
        sign_info = SignInfo(private=private_key, public=public_key)
        sdk_info = SdkInfo(annotators=[], hash=HashInfo(type=hash), signature=sign_info, stream=[])

        annotator = AnnotatorFactory().get_annotator(kind=kind, sdk_info=sdk_info)

        test_data = b"test data"
        result = annotator.execute(data=test_data)
        self.assertEqual(kind, result.kind)
        self.assertEqual(hash, result.hash)
        self.assertIsNotNone(result.signature)
        # Source annotator is_satisfied should always be true
        self.assertEqual(True, result.is_satisfied)

if __name__ == "__main__":
    unittest.main()