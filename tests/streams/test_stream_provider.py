import unittest

from alvarium.streams.contracts import StreamInfo, StreamType
from alvarium.streams.factories import StreamProviderFactory
from alvarium.contracts.publish import PublishWrapper, SdkAction

class TestStreamProvider(unittest.TestCase):

    def test_mock_provider_connect_should_return_none(self):
        stream_info = StreamInfo(type=StreamType.MOCK, config={})

        factory = StreamProviderFactory()
        provider = factory.getProvider(info=stream_info)

        result = provider.connect()
        self.assertEqual(result, None)
    
    def test_mock_provider_close_should_return_none(self):
        stream_info = StreamInfo(type=StreamType.MOCK, config={})

        factory = StreamProviderFactory()
        provider = factory.getProvider(info=stream_info)

        result = provider.close()
        self.assertEqual(result, None)

    def test_mock_provider_publish_should_return_none(self):
        stream_info = StreamInfo(type=StreamType.MOCK, config={})
        wrapper = PublishWrapper(action=SdkAction.CREATE, message_type=str(dict), content={})

        factory = StreamProviderFactory()
        provider = factory.getProvider(info=stream_info)

        result = provider.publish(wrapper=wrapper)
        self.assertEqual(result, None)

if __name__ == "__main__":
    unittest.main()