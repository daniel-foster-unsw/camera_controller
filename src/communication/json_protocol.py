"""
json_protocol.py

JSON serialisation/deserialisation for the Camera Controller protocol.
"""

import json

from communication.command import Command


class JsonProtocol:

    @staticmethod
    def deserialize(message: str) -> Command:

        data = json.loads(message)

        return Command(

            version=data["version"],

            command=data["command"],

            parameters=data.get("parameters", {})

        )


    @staticmethod
    def serialize(response):

        return response.to_json()