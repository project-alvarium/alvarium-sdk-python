from abc import ABC, abstractmethod

class PropertyBag(ABC):

    @abstractmethod
    def getProperty(self, key: str): 
        pass

    @abstractmethod
    def toMap(self) -> dict:
        pass

class ImmutablePropertyBag(PropertyBag):

    def __init__(self, bag: dict) -> None:
        self.bag = bag

    def getProperty(self, key: str):
        if key in self.bag:
            return self.bag.get(key)
        else:
            raise ValueError(f'Property {key} not found')

    def toMap(self):
        return self.bag