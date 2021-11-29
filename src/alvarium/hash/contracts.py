from enum import Enum
from dataclasses import dataclass
import json

class HashType(Enum):

    NONE = "none"
    MD5 = "md5"
    SHA256 = "sha256"

    def __str__(self) -> str:
        return f'{self.value}' 

@dataclass
class HashInfo():
    """A data class that encapsulates the config related to hash opertations."""

    type: HashType

    def to_json(self) -> str:
        info_json = {"type": str(self.type)}
        return json.dumps(info_json)
    
    @staticmethod
    def from_json(data: str):
        info_json = json.loads(data)
        return HashInfo(type=HashType(info_json["type"]))
    
    def __str__(self) -> str:
        self.to_json() 
