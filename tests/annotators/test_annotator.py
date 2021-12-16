import unittest

from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.contracts.config import SdkInfo
from alvarium.hash.contracts import HashInfo, HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType
from alvarium.annotators.factories import AnnotatorFactory
from alvarium.utils import ImmutablePropertyBag

class AnnotatorTest(unittest.TestCase):

    def test_mock_Annotator_Should_Return_Annotation(self):
        keyInfo = KeyInfo(type=SignType.NONE,path="path")
        signature = SignInfo(keyInfo, keyInfo)
        sdk_info = SdkInfo(annotators=[], hash=HashInfo(type=HashType.MD5), signature=signature, stream=None)
        factory = AnnotatorFactory()
        annotator = factory.getAnnotator(kind=AnnotationType.MOCK,sdk_info=sdk_info)
        string = "test data"
        data = bytearray(string.encode())
        ctx = ImmutablePropertyBag({})
        annotation = annotator.execute(data=data, ctx=ctx)

        self.assertEqual(type(annotation), Annotation)

if __name__ == "__main__":
    unittest.main()