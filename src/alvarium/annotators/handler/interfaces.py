from abc import ABC, abstractmethod
import datetime
from typing import List
from alvarium.sign.contracts import SignInfo

class RequestHandler(ABC):

    @abstractmethod
    def AddSignatureHeaders(self, ticks: datetime, fields: List[str], keys: SignInfo) -> None:
        pass