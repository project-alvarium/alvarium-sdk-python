import json
import base64

from enum import Enum
from dataclasses import dataclass
from typing import Any

class SdkAction(Enum):

    CREATE = "create"
    MUTATE = "mutate"
    TRANSIT = "transit"

    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class PublishWrapper:
    """A data class that encapsulates the data being published by stream providers"""

    action: SdkAction
    message_type: str
    content: Any

    def to_json(self) -> str:
        # content is first encoded to base64 to match the go sdk implementation
        content = base64.b64encode(bytes(str(self.content), 'utf-8')).decode('utf-8')
        wrapper_json = {"action": str(self.action), "messageType": str(self.message_type), 
                        "content": str(content)}
        return json.dumps(wrapper_json)
    
    def __str__(self) -> str:
        return self.to_json()