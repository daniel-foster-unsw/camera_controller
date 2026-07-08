"""
response.py

Represents a response returned to the PC.
"""
from dataclasses import dataclass, asdict
import json

@dataclass
class Response:

    version: str
    status: str
    message: str
    data: dict | None = None
    
    def to_json(self):

        return json.dumps(asdict(self))