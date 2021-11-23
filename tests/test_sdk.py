import unittest

from alvarium.sdk import Sdk

class MockSdk(Sdk):
    """mock implementation of the sdk interface"""

    def create(self, data, properties=None) -> None:
        print("data created")

    def mutate(self, old_data, new_data, properties=None) -> None:
        print("data mutated")

    def transit(self, data, properties=None) -> None:
        print("data transitioned")
    
    def close(self) -> None:
        print("sdk disposed")

class TestSdk(unittest.TestCase):
    
    def setUp(self) -> None:
        self.sdk = MockSdk()

    def test_sdk_should_create(self) -> None:
        """always true test case"""
        self.sdk.create(data=[])
        self.assertTrue(True)
    
    def tearDown(self) -> None:
        self.sdk.close()

if __name__ == "__main__":
    unittest.main()