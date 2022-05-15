from dataclasses import dataclass
from enum import Enum


class DerivedComponent(Enum):
    Method = "@method"
    TargetURI = "@target-uri"
    Authority = "@authority"
    Scheme = "@scheme"
    Path = "@path"
    Query = "@query"
    QueryParams = "@query-params"

    def __str__(self) -> str:
        return f'{self.value}'

class HttpConstants:

    @property
    def http_request_key(self):
        return "HttpRequestKey"

    @property
    def content_type(self):
        return "Content-Type"

    @property
    def content_length(self):
        return "Content-Length"

@dataclass
class ParseResult:
    """A data class that holds the parsed data"""

    seed: str
    signature: str
    keyid: str
    algorithm: str

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ParseResult):
            return NotImplemented
        return self.seed == __o.seed and self.signature == __o.signature and self.keyid == __o.keyid and self.algorithm == __o.algorithm