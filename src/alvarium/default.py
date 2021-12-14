from logging import Logger
from typing import List
from .sdk import Sdk
from .utils import PropertyBag
from .streams.factories import StreamProviderFactory
from .annotators.interfaces import Annotator
from .contracts.config import SdkInfo

class DefaultSdk(Sdk):
    """default implementation of the sdk interface"""
    
    def __init__(self, annotators: List[Annotator], config: SdkInfo, logger: Logger) -> None:
        self.annotators = annotators
        self.config = config

        self.stream = StreamProviderFactory().getProvider(self.config.stream)
        self.stream.connect()

        self.logger = logger
        self.logger.debug("stream provider connected successfully")

    def create(self, data: bytes, properties: PropertyBag = None) -> None:
        self.logger.debug("data created")

    def mutate(self, old_data: bytes, new_data: bytes, properties: PropertyBag = None) -> None:
        self.logger.debug("data mutated")

    def transit(self, data: bytes, properties: PropertyBag = None) -> None:
        self.logger.debug("data transitioned")
    
    def close(self) -> None:
        self.stream.close()
        self.logger.debug("sdk disposed")

