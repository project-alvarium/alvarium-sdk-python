import unittest, json, logging
from typing import List
from alvarium.contracts.config import SdkInfo
from alvarium.annotators.interfaces import Annotator
from alvarium.annotators.factories import AnnotatorFactory
from alvarium.sdk import Sdk
from alvarium.default import DefaultSdk

class TestSdk(unittest.TestCase):

    def setUp(self) -> None:
        self.test_json = {}
        with open("./tests/mock-info.json", "r") as file:
            self.test_json = json.loads(file.read())

    def test_default_sdk_instantiate_should_not_raise(self):
        sdk_info: SdkInfo = SdkInfo.from_json(json.dumps(self.test_json))
        annotator_factory = AnnotatorFactory()
        annotators = [annotator_factory.get_annotator(kind=annotation_type, sdk_info=sdk_info) for annotation_type in sdk_info.annotators]

        logger = logging.getLogger(__name__)
        logging.basicConfig(level = logging.DEBUG)

        sdk: Sdk = DefaultSdk(annotators=annotators,config=sdk_info,logger=logger)
        sdk.close()

    def test_sdk_should_create(self):
        sdk_info: SdkInfo = SdkInfo.from_json(json.dumps(self.test_json))
        annotator_factory = AnnotatorFactory()
        annotators = [annotator_factory.get_annotator(kind=annotation_type, sdk_info=sdk_info) for annotation_type in sdk_info.annotators]

        logger = logging.getLogger(__name__)
        logging.basicConfig(level = logging.DEBUG)
        sdk = DefaultSdk(annotators=annotators, config=sdk_info, logger=logger)

        test_data = b'test'
        sdk.create(data=test_data)
        sdk.close()
    
    def test_sdk_should_mutate(self):
        sdk_info: SdkInfo = SdkInfo.from_json(json.dumps(self.test_json))
        annotator_factory = AnnotatorFactory()
        annotators = [annotator_factory.get_annotator(kind=annotation_type, sdk_info=sdk_info) for annotation_type in sdk_info.annotators]

        logger = logging.getLogger(__name__)
        logging.basicConfig(level = logging.DEBUG)
        sdk = DefaultSdk(annotators=annotators, config=sdk_info, logger=logger)

        old_data = b'old data'
        new_data = b'new data'
        sdk.mutate(old_data=old_data, new_data=new_data)
        sdk.close()


    def test_sdk_should_transit(self) -> None:
        sdk_info: SdkInfo = SdkInfo.from_json(json.dumps(self.test_json))
        annotator_factory = AnnotatorFactory()
        annotators = [annotator_factory.get_annotator(kind=annotation_type, sdk_info=sdk_info) for annotation_type in sdk_info.annotators]

        logger = logging.getLogger(__name__)
        logging.basicConfig(level = logging.DEBUG)
        sdk = DefaultSdk(annotators=annotators, config=sdk_info, logger=logger)

        test_data = b'test'
        sdk.transit(data=test_data)
        sdk.close()

if __name__ == "__main__":
    unittest.main()