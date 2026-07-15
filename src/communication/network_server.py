"""
network_server.py

TCP communication server for the Camera Controller.
"""

import socket


class NetworkServer:

    def __init__(self, host="0.0.0.0", port=5000):

        self.host = host
        self.port = port

        self.server = None
        self.connection = None
        self.address = None

    def initialise(self):

        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.server.bind(
            (self.host, self.port)
        )

        self.server.listen(1)

        print(
            f"Listening on {self.host}:{self.port}"
        )

    def wait_for_client(self):

        self.connection, self.address = self.server.accept()

        print(
            f"Client connected: {self.address}"
        )

    def stop(self):

        if self.connection:
            self.connection.close()

        if self.server:
            self.server.close()