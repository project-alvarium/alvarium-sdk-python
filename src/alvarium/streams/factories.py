from alvarium.streams.exceptions import StreamException
from alvarium.streams.mock import MockProvider
from alvarium.streams.mqtt_stream_provider import MQTTStreamProvider
from .contracts import StreamInfo, StreamType

class StreamProviderFactory:
    """A factory that returns a specific implementation of a StreamProvider"""

    def getProvider(self, info: StreamInfo):
        if info.type == StreamType.MOCK:
            return MockProvider()
        if info.type == StreamType.MQTT:
            return MQTTStreamProvider(info.config)
        else:
            raise StreamException(f"{info.type} is not yet implemented.")