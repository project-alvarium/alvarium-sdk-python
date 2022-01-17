from dataclasses import dataclass
from enum import Enum
import json 

class SignType(Enum):

    ED25519 = "ed25519"
    NONE = "none"

    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class KeyInfo:
    """A data class that encapsulates the config related to key info"""
    type: SignType
    path: str

    def to_json(self) -> str:
        info_json = {"type" : str(self.type), "path": self.path} 
        return json.dumps(info_json)
    
    @staticmethod
    def from_json(data: str):
        info_json = json.loads(data)
        return KeyInfo(type = SignType(info_json["type"]), path=info_json["path"])
    
    
    def __str__(self) -> str:
        return self.to_json()

@dataclass
class SignInfo:
    """A data class that encapsulates the config related to sign opertations."""
    public: KeyInfo
    private: KeyInfo
    
    def to_json(self) -> str:
        info_json = {}
        info_json["public"] = json.loads(self.public.to_json())
        info_json["private"] = json.loads(self.private.to_json())
        return json.dumps(info_json)
    
    @staticmethod
    def from_json(data: str):
        info_json = json.loads(data) 
        return SignInfo(public = KeyInfo.from_json(json.dumps(info_json["public"])),
                            private = KeyInfo.from_json(json.dumps(info_json["private"])))
                            
    def __str__(self) -> str:
        return self.to_json()