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

    def test_default_sdk_instantiate_should_not_raise(self):
        sdk_info: SdkInfo = SdkInfo.from_json(json.dumps(self.test_json))
        
        annotators: List[Annotator] = []
        for i in range (0,len(sdk_info.annotators)):
            annotators.append(AnnotatorFactory().getAnnotator(kind=sdk_info.annotators[i], sdk_info=sdk_info))

        logger = logging.getLogger(__name__)
        logging.basicConfig(level = logging.DEBUG)

        sdk: Sdk = DefaultSdk(annotators=annotators,config=sdk_info,logger=logger)
        sdk.close()

    def test_sdk_should_create(self) -> None:
        sdk_info: SdkInfo = SdkInfo.from_json(json.dumps(self.test_json))
        annotator_factory = AnnotatorFactory()
        annotators = [annotator_factory.getAnnotator(kind=annotation_type, sdk_info=sdk_info) for annotation_type in sdk_info.annotators]

        logger = logging.getLogger(__name__)
        logging.basicConfig(level = logging.DEBUG)
        sdk = DefaultSdk(annotators=annotators, config=sdk_info, logger=logger)

        test_data = b'test'
        sdk.create(data=test_data)
        sdk.close()

    def test_sdk_should_transit(self) -> None:
        sdk_info: SdkInfo = SdkInfo.from_json(json.dumps(self.test_json))
        annotator_factory = AnnotatorFactory()
        annotators = [annotator_factory.getAnnotator(kind=annotation_type, sdk_info=sdk_info) for annotation_type in sdk_info.annotators]

        logger = logging.getLogger(__name__)
        logging.basicConfig(level = logging.DEBUG)
        sdk = DefaultSdk(annotators=annotators, config=sdk_info, logger=logger)

        test_data = b'test'
        sdk.transit(data=test_data)
        sdk.close()

if __name__ == "__main__":
    unittest.main()