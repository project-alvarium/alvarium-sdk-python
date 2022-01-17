from abc import ABC, abstractmethod

class PropertyBag(ABC):

    @abstractmethod
    def get_property(self, key: str): 
        pass

    @abstractmethod
    def to_map(self) -> dict:
        pass

class ImmutablePropertyBag(PropertyBag):

    def __init__(self, bag: dict) -> None:
        self.bag = bag

    def get_property(self, key: str):
        if key in self.bag:
            return self.bag.get(key)
        else:
            raise ValueError(f'Property {key} not found')

    def to_map(self) -> dict:
        return self.bag