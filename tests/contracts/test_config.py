import unittest
import json
from alvarium.contracts.annotation import AnnotationType

from alvarium.contracts.config import SdkInfo
from alvarium.hash.contracts import HashInfo, HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType
from alvarium.streams.contracts import MQTTConfig, ServiceInfo, StreamInfo, StreamType

class TestConfig(unittest.TestCase):

    def test_sdk_info_from_json_should_return_sdk_info(self):
        annotators = [AnnotationType.TLS, AnnotationType.MOCK]
        hash = HashInfo(type=HashType.SHA256)
        signature = SignInfo(public=KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/public.key"),
                             private=KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key"))
        stream = StreamInfo(type=StreamType.MQTT, config=MQTTConfig(client_id="alvarium-test", qos=0, user="",
                            password="", is_clean=False, topics=["alvarium-test-topic"], provider=ServiceInfo(
                                host="test.mosquitto.org", port=1883, protocol="tcp"
                            )))

        test_json = {}
        with open("./tests/contracts/sdk-info.json", "r") as file:
            test_json = json.loads(file.read())
        
        result = SdkInfo.from_json(json.dumps(test_json))
        self.assertEqual(result.annotators, annotators)
        self.assertEqual(result.hash, hash)
        self.assertEqual(result.signature, signature)
        self.assertEqual(result.stream, stream)

    def test_sdk_info_to_json_should_return_right_representation(self):
        annotators = [AnnotationType.TLS, AnnotationType.MOCK]
        hash = HashInfo(type=HashType.SHA256)
        signature = SignInfo(public=KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/public.key"),
                             private=KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key"))
        stream = StreamInfo(type=StreamType.MQTT, config=MQTTConfig(client_id="alvarium-test", qos=0, user="",
                            password="", is_clean=False, topics=["alvarium-test-topic"], provider=ServiceInfo(
                                host="test.mosquitto.org", port=1883, protocol="tcp"
                            )))
        
        sdk_info = SdkInfo(annotators=annotators, hash=hash, signature=signature, stream=stream)
        result = json.loads(sdk_info.to_json())
        
        test_json = {}
        with open("./tests/contracts/sdk-info.json", "r") as file:
            test_json = json.loads(file.read())

        self.assertEqual(result["annotators"], test_json["annotators"])
        self.assertEqual(result["hash"], test_json["hash"])
        self.assertEqual(result["signature"], test_json["signature"])
        self.assertEqual(result["stream"], test_json["stream"])


if __name__ == "__main__":
    unittest.main()