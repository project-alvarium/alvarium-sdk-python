from logging import Logger
from typing import List
from .sdk import Sdk
from .utils import PropertyBag
from .streams.factories import StreamProviderFactory
from .annotators.interfaces import Annotator
from .contracts.config import SdkInfo
from .contracts.annotation import AnnotationList
from .contracts.publish import PublishWrapper, SdkAction

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
        annotation_list = AnnotationList(items=[ann.execute(data=data, ctx=properties) for ann in self.annotators])
        wrapper = PublishWrapper(action=SdkAction.CREATE, message_type=type(annotation_list).__name__, content=annotation_list)

        self.stream.publish(wrapper=wrapper)
        self.logger.debug("data annotated and published successfully.")


    def mutate(self, old_data: bytes, new_data: bytes, properties: PropertyBag = None) -> None:
        self.logger.debug("data mutated")

    def transit(self, data: bytes, properties: PropertyBag = None) -> None:
        self.logger.debug("data transitioned")
    
    def close(self) -> None:
        self.stream.close()
        self.logger.debug("sdk disposed")

