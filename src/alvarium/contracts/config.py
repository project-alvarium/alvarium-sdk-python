import json

from dataclasses import dataclass
from typing import List
from alvarium.hash.contracts import HashInfo
from alvarium.sign.contracts import SignInfo
from alvarium.streams.contracts import StreamInfo
from .annotation import AnnotationType

@dataclass
class SdkInfo:
    """A data class that encapsulates all of the config related to the SDK"""

    annotators: List[AnnotationType]
    hash: HashInfo
    signature: SignInfo
    stream: StreamInfo

    @staticmethod
    def from_json(data: str):
        info_json = json.loads(data)
        annotators = [AnnotationType(x) for x in info_json["annotators"]]
        hash = HashInfo.from_json(json.dumps(info_json["hash"]))
        signature = SignInfo.from_json(json.dumps(info_json["signature"]))
        stream = StreamInfo.from_json(json.dumps(info_json["stream"]))
        return SdkInfo(annotators=annotators, hash=hash, signature=signature, stream=stream)

    def to_json(self) -> str:
        info_json = {}
        info_json["annotators"] = [str(x) for x in self.annotators]
        info_json["hash"] = json.loads(self.hash.to_json())
        info_json["signature"] = json.loads(self.signature.to_json())
        info_json["stream"] = json.loads(self.stream.to_json())
        return json.dumps(info_json)
    
    def __str__(self) -> str:
        return self.to_json()