import unittest

from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType
from alvarium.annotators.factories import AnnotatorFactory
from alvarium.utils import ImmutablePropertyBag

class AnnotatorTest(unittest.TestCase):

    def test_mock_Annotator_Should_Return_Annotation(self):
        keyInfo = KeyInfo(type=SignType.NONE,path="path")
        signature = SignInfo(keyInfo, keyInfo)
        factory = AnnotatorFactory()
        annotator = factory.getAnnotator(kind=AnnotationType.MOCK,hash=HashType.MD5,signature=signature)
        string = "test data"
        data = bytearray(string.encode())
        ctx = ImmutablePropertyBag({})
        annotation = annotator.execute(data=data, ctx=ctx)

        self.assertEqual(type(annotation), Annotation)

if __name__ == "__main__":
    unittest.main()