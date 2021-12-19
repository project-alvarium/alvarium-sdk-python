import unittest
import json

from alvarium.streams.contracts import ServiceInfo, StreamInfo, StreamType

class TestStreamInfo(unittest.TestCase):

    def test_to_json_should_return_json_representation(self):
        stream_info = StreamInfo(type=StreamType.MQTT, config={})
        result = stream_info.to_json()

        info_json = json.loads(result)
        self.assertEqual(StreamType(info_json["type"]), StreamType.MQTT)
        self.assertEqual(info_json["config"], {})
    
    def test_from_json_should_return_stream_info(self):
        info_json = {}

        with open("./tests/streams/config-mqtt.json") as file:
            info_json = json.loads(file.read())
        
        stream_info = StreamInfo.from_json(json.dumps(info_json))
        self.assertEqual(StreamType.MQTT, stream_info.type)

class TestServiceInfo(unittest.TestCase):

    def test_to_json_should_return_json_representation(self):
        host = "localhost"
        protocol = "tcp"
        port = 1883
        service_info = ServiceInfo(host=host, protocol=protocol, port=port)
        result = service_info.to_json()

        info_json = json.loads(result)
        self.assertEqual(host, info_json["host"])
        self.assertEqual(protocol, info_json["protocol"])
        self.assertEqual(port, info_json["port"])
    
    def test_from_json_should_return_service_info_object(self):
        host = "localhost"
        protocol = "tcp"
        port = 1883
        info_json = {}
        with open("./tests/streams/service-info.json") as file:
            info_json = json.loads(file.read())
        
        result = ServiceInfo.from_json(json.dumps(info_json))

        self.assertEqual(result.host, host)
        self.assertEqual(result.protocol, protocol)
        self.assertEqual(result.port, port)
    
    def test_uri_should_return_the_right_representation(self):
        host = "localhost"
        protocol = "tcp"
        port = 1883

        service_info = ServiceInfo(host=host, protocol=protocol, port=port)
        uri = service_info.uri()
        self.assertEqual(f"{protocol}://{host}:{port}", uri)


if __name__ == "__main__":
    unittest.main()
