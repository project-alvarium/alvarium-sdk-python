import unittest, json, logging
from typing import List
from alvarium.contracts.config import SdkInfo
from alvarium.annotators.interfaces import Annotator
from alvarium.annotators.factories import AnnotatorFactory
from alvarium.sdk import Sdk
from alvarium.default import DefaultSdk

class MockSdk(Sdk):
    """mock implementation of the sdk interface"""

    def create(self, data: bytes, properties=None) -> None:
        pass

    def mutate(self, old_data: bytes, new_data: bytes, properties=None) -> None:
        pass
    
    def transit(self, data: bytes, properties=None) -> None:
        pass

    def close(self) -> None:
        pass

class TestSdk(unittest.TestCase):

    def setUp(self) -> None:
        self.test_json = {}
        with open("./tests/mock-info.json", "r") as file:
            self.test_json = json.loads(file.read())
        self.sdk = MockSdk()

    def test_default_sdk_instantiate_should_not_raise(self):
        sdkInfo: SdkInfo = SdkInfo.from_json(json.dumps(self.test_json))
        
        annotators: List[Annotator] = []
        for i in range (0,len(sdkInfo.annotators)):
            annotators.append(AnnotatorFactory().getAnnotator(kind = sdkInfo.annotators[i],hash = sdkInfo.hash, signature = sdkInfo.signature))

        logger = logging.getLogger(__name__)
        logging.basicConfig(level = logging.DEBUG)

        sdk: Sdk = DefaultSdk(annotators, sdkInfo, logger)
        sdk.close()

    def test_sdk_should_create(self) -> None:
        """always true test case"""
        self.sdk.create(data=b'test')
        self.assertTrue(True)
    
    def tearDown(self) -> None:
        self.sdk.close()

if __name__ == "__main__":
    unittest.main()