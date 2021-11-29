from .sdk import Sdk

class DefaultSdk(Sdk):
    """default implementation of the sdk interface"""

    def create(self, data: bytes, properties=None) -> None:
        print("data created")

    def mutate(self, old_data: bytes, new_data: bytes, properties=None) -> None:
        print("data mutated")

    def transit(self, data: bytes, properties=None) -> None:
        print("data transitioned")
    
    def close(self) -> None:
        print("sdk disposed")

