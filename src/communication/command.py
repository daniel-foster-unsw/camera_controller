"""
command.py

Represents a command received over USB.
"""

from dataclasses import dataclass
import json

@dataclass
class Command:

    version: str
    command: str
    parameters: dict | None = None

    @classmethod
    def from_json(cls, json_string):
        """Create a Command instance from a JSON string."""

        data = json.loads(json_string)

        return cls(
            version=data["version"],
            command=data["command"],
            parameters=data.get("parameters")
        )