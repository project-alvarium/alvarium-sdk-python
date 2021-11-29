import unittest

from alvarium.sdk import Sdk

class MockSdk(Sdk):
    """mock implementation of the sdk interface"""

    def create(self, data: bytes, properties=None) -> None:
        pass

    def mutate(self, old_data: bytes, new_data: bytes, properties=None) -> None:
        pass
    
    def transit(self, data: bytes, properties=None) -> None:
        pass

    def close(self) -> None:
        pass
class TestSdk(unittest.TestCase):
    
    def setUp(self) -> None:
        self.sdk = MockSdk()

    def test_sdk_should_create(self) -> None:
        """always true test case"""
        self.sdk.create(data=b'test')
        self.assertTrue(True)
    
    def tearDown(self) -> None:
        self.sdk.close()

if __name__ == "__main__":
    unittest.main()