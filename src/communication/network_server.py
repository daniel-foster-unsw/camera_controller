"""
network_server.py

TCP communication server for the Camera Controller.
"""

import socket
from communication.communication_interface import CommunicationInterface


class NetworkServer(CommunicationInterface):

    def __init__(self, host="0.0.0.0", port=5000):

        self.host = host
        self.port = port

        self.server = None
        self.connection = None
        self.address = None

    def initialise(self, configuration=None, logger=None):
        self.configuration = configuration
        self.logger = logger

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

        self.reader = self.connection.makefile(
        "r",
        encoding="utf-8"
        )

        self.writer = self.connection.makefile(
            "w",
            encoding="utf-8"
        )

        print(
            f"Client connected: {self.address}"
        )
        
    def stop(self):

        if hasattr(self, "reader"):
            self.reader.close()

        if hasattr(self, "writer"):
            self.writer.close()

        if self.connection:
            self.connection.close()

        if self.server:
            self.server.close()


    def receive(self):

        return self.reader.readline().strip()
    
    def send(self, message):
               

        self.writer.write(message + "\n")

        self.writer.flush()

    def send_bytes(self, data: bytes):
        """
        Send binary data over the existing TCP connection.
        """
        if self.connection is None:
            raise ConnectionError("No client connected.")
        self.connection.sendall(data)


    def close_client(self):

        if hasattr(self, "reader") and self.reader:
            self.reader.close()
            self.reader = None

        if hasattr(self, "writer") and self.writer:
            self.writer.close()
            self.writer = None

        if hasattr(self, "connection") and self.connection:
            self.connection.close()
            self.connection = None

        self.address = None

    def close(self):
        
        self.close_client()

        if hasattr(self, "server") and self.server:
            self.server.close()
            self.server = None