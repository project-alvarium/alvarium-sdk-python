import unittest
from alvarium.streams.contracts import StreamInfo, MQTTConfig
import json

from alvarium.streams.factories import StreamProviderFactory
from alvarium.contracts.publish import PublishWrapper, SdkAction

class TestMQTTStreamProvider(unittest.TestCase):

    def should_load_config(self):
        config_path = 'tests/streams/config-mqtt.json'
        
        with open(config_path, "r") as file:
            config_json = file.read()
        
        stream_info = StreamInfo.from_json(config_json)
        mqtt_config = stream_info.config 
        self.assertIsNotNone(mqtt_config)

    def mqtt_should_connect(self):
        config_path = 'tests/streams/config-mqtt.json'
        
        with open(config_path, "r") as file:
            config_json = file.read()
        
        stream_info = StreamInfo.from_json(config_json)

        factory = StreamProviderFactory()
        provider = factory.getProvider(info=stream_info)

        provider.connect()
    
    def mqtt_should_publish(self):
        config_path = 'tests/streams/config-mqtt.json'
        
        with open(config_path, "r") as file:
            config_json = file.read()
        
        stream_info = StreamInfo.from_json(config_json)

        factory = StreamProviderFactory()
        provider = factory.getProvider(info=stream_info)

        provider.connect()
        msg = '{ "content" : "connected"}'
        test_publish_wrapper = PublishWrapper( SdkAction.CREATE, message_type="str", content= msg  )

        provider.publish(test_publish_wrapper)

    def mqtt_should_close(self):
        config_path = 'tests/streams/config-mqtt.json'
        
        with open(config_path, "r") as file:
            config_json = file.read()
        
        stream_info = StreamInfo.from_json(config_json)

        factory = StreamProviderFactory()
        provider = factory.getProvider(info=stream_info)

        provider.connect()

        msg = '{ "content" : "closing"}'
        test_publish_wrapper = PublishWrapper( SdkAction.CREATE, message_type="str", content= msg  )

        provider.publish(test_publish_wrapper)
        provider.close()



