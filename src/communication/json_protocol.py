"""
json_protocol.py

JSON serialisation/deserialisation for the Camera Controller protocol.
"""

import json

from communication.command import Command


class JsonProtocol:

    @staticmethod
    def deserialize(message: str) -> Command:
        """
        Convert a JSON string into a Command object.
        """

        data = json.loads(message)

        return Command(
            version=data.get("version"),
            command=data.get("command"),
            parameters=data.get("parameters", {})
        )


    @staticmethod
    def serialize(response) -> str:
        """
        Convert a Response object into a JSON string.
        """
        return response.to_json()