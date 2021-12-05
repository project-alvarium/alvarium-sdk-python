import json

from enum import Enum
from dataclasses import dataclass
from typing import Any


class StreamType(Enum):

    MOCK = "mock"
    MQTT = "mqtt"

    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class StreamInfo:
    """A data class that encapsulates the type and config of the stream provider"""

    type: StreamType
    config: Any

    @staticmethod
    def from_json(data: str):
        # TODO (karim elghamry): add  type check to config and parse accordingly
        info_json = json.loads(data)
        return StreamInfo(type=StreamType(info_json["type"]), config=info_json["config"])
    
    def to_json(self) -> str:
        info_json = {"type": str(self.type), "config": json.loads(str(self.config))}
        return json.dumps(info_json)
    
    def __str__(self) -> str:
        self.to_json()

@dataclass
class ServiceInfo:
    """A data class that encapsulates the uri related data of a stream provider"""

    host: str
    protocol: str
    port:  int

    def uri(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"

    @staticmethod
    def from_json(data: str):
        info_json = json.loads(data)
        return ServiceInfo(host=info_json["host"], protocol=info_json["protocol"], port=info_json["port"])
    
    def to_json(self) -> str:
        info_json = {"host": self.host, "protocol": self.protocol, "port": self.port}
        return json.dumps(info_json)
    
    def __str__(self) -> str:
        return self.to_json()
