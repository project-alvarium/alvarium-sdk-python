from .exceptions import StreamException
from .mock import MockProvider
from .mqtt import MQTTStreamProvider
from .contracts import StreamInfo, StreamType

class StreamProviderFactory:
    """A factory that returns a specific implementation of a StreamProvider"""

    def get_provider(self, info: StreamInfo):
        if info.type == StreamType.MOCK:
            return MockProvider()
        if info.type == StreamType.MQTT:
            return MQTTStreamProvider(info.config)
        else:
            raise StreamException(f"{info.type} is not yet implemented.")