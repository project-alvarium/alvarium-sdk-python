import base64
import unittest
import json
from alvarium.contracts.annotation import Annotation, AnnotationList, AnnotationType

from alvarium.contracts.publish import PublishWrapper, SdkAction
from alvarium.hash.contracts import HashType

class TestPublishWrapper(unittest.TestCase):

    def test_to_json_should_return_json_representation(self):
        annotation = Annotation(key="key", hash=HashType.NONE, host="host", kind=AnnotationType.MOCK,
                                is_satisfied=True, signature="signature")
        action = SdkAction.CREATE
        content = AnnotationList(items=[annotation, annotation]) 
        message_type = str(type(content))
        wrapper = PublishWrapper(action=action, message_type=message_type, content=content)

        result = wrapper.to_json()
        wrapper_json = json.loads(result)

        self.assertEqual(SdkAction(wrapper_json["action"]), action)
        self.assertEqual(wrapper_json["messageType"], message_type)
        self.assertEqual(wrapper_json["content"], base64.b64encode(bytes(str(content), 'utf-8')).decode('utf-8'))

if __name__ == "__main__":
    unittest.main()