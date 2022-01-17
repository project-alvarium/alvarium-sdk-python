from .interfaces import StreamProvider
from alvarium.contracts.publish import PublishWrapper

class MockProvider(StreamProvider):
    """mock implementation of the StreamProvider interface"""

    def connect(self) -> None:
        pass

    def close(self) -> None:
        pass

    def publish(self, wrapper: PublishWrapper) -> None:
        wrapper.to_json()
        pass