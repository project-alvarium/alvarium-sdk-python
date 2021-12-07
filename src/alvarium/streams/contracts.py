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
        info_json = json.loads(data)
        if (info_json["type"] == str(StreamType.MOCK)):
            return StreamInfo(type=StreamType(info_json["type"]), config=info_json["config"])
        elif( info_json["type"] == str(StreamType.MQTT)):
            return StreamInfo(type=StreamType(info_json["type"]), config=MQTTConfig.from_json( json.dumps(info_json["config"])))

    
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


@dataclass
class MQTTConfig:
    """A data class that encapsulates the MQTT Configuration"""

    clientId: str
    user: str
    password: str
    qos: int
    isClean: bool
    topics: list
    provider: ServiceInfo

    @staticmethod
    def from_json(data: str):
        info_json = json.loads(data)
        return MQTTConfig(clientId=info_json["clientId"],
                          user=info_json["user"],
                          password=info_json["password"],
                          qos=info_json["qos"],
                          isClean=info_json["cleanness"],
                          topics=info_json["topics"],
                          provider= ServiceInfo.from_json ( json.dumps (info_json["provider"])))

    def to_json(self) -> str:
        info_json = {"clientId": self.clientId,
                     "user": self.user,
                     "password": self.password,
                     "qos": self.qos,
                     "cleanness": self.isClean,
                     "topics": self.topics,
                     "provider": json.loads(self.provider.to_json())
                     }
        return json.dumps(info_json)

    def __str__(self) -> str:
        return self.to_json()
