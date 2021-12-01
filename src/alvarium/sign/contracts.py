from dataclasses import dataclass
from enum import Enum
import json 

class SignType(Enum):
    """Enum decleration for Sign type"""
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
        infoJson = {"type" : str(self.type), "path": self.path} 
        return json.dumps(infoJson)
    
    @staticmethod
    def from_json(data: str):
        infoData = json.loads(data)
        return KeyInfo(type = SignType(infoData["type"]), path=infoData["path"])
    
    
    def __str__(self) -> str:
        return self.to_json()

@dataclass
class SignInfo:
    """A data class that encapsulates the config related to sign opertations."""
    public: KeyInfo
    private: KeyInfo
    
    def to_json(self) -> str:
        infoJson={}
        infoJson["public"] = json.loads(self.public.to_json())
        infoJson["private"] = json.loads(self.private.to_json())
        return json.dumps(infoJson)
    
    @staticmethod
    def from_json(data: str):
        infoData = json.loads(data) 
        return SignInfo(public = KeyInfo.from_json(json.dumps(infoData["public"])),
                            private = KeyInfo.from_json(json.dumps(infoData["private"])))
                            
    def __str__(self) -> str:
        return self.to_json()
    



