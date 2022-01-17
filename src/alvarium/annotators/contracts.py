import json

from dataclasses import dataclass

@dataclass
class Signable:
    """A data class that holds the seed (data) and signature for this data"""

    seed: str
    signature: str

    @staticmethod
    def from_json(data: str):
        signable_json = json.loads(data)
        return Signable(seed=str(signable_json["seed"]), signature=str(signable_json["signature"]))
    
    def to_json(self) -> str:
        signable_json = {
            "seed": str(self.seed),
            "signature": str(self.signature)
        }
        return json.dumps(signable_json)
    
    def __str__(self) -> str:
        return self.to_json()