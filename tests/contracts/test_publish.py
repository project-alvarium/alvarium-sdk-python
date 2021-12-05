import unittest
import json

from alvarium.contracts.publish import PublishWrapper, SdkAction

class TestPublishWrapper(unittest.TestCase):

    def test_to_json_should_return_json_representation(self):
        action = SdkAction.CREATE
        content = {}
        message_type = str(type(content))
        wrapper = PublishWrapper(action=action, message_type=message_type, content=content)

        result = wrapper.to_json()
        wrapper_json = json.loads(result)

        self.assertEqual(SdkAction(wrapper_json["action"]), action)
        self.assertEqual(wrapper_json["messageType"], message_type)
        self.assertEqual(wrapper_json["content"], content)

if __name__ == "__main__":
    unittest.main()