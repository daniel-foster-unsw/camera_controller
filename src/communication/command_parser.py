"""
command_parser.py

Parses commands received over USB.
"""
from communication.protocol import (
    PROTOCOL_VERSION,
    PING,
    STATUS_OK,
    STATUS_ERROR
)

from response import Response

class CommandParser:

    def __init__(self, application):

        self.application = application


    def execute(self, command):

        if command.command == "PING":

            return Response(
                version=PROTOCOL_VERSION,
                status=STATUS_OK,
                message="PONG"
            )
        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_ERROR,
            message=f"Unknown command: {command.command}"
        )

        raise ValueError(
            f"Unknown command: {command.command}"
        )