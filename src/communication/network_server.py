"""
network_server.py

TCP communication server for the Camera Controller.
"""

import socket
from communication.communication_interface import CommunicationInterface


class NetworkServer(CommunicationInterface):

    def __init__(self, host="0.0.0.0", port=5000):
        """
        Initialise the TCP network server.
        """
        self.host = host
        self.port = port

        self.server = None
        self.connection = None
        self.address = None

    def initialise(self, configuration=None, logger=None):
        """
        Create and configure the TCP server socket.
        """
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

        print(f"Host = {self.host}")
        print(f"Port = {self.port}")

        self.server.bind(
            (self.host, self.port)
        )

        self.server.listen(1)

        print(
            f"Listening on {self.host}:{self.port}"
        )

    def wait_for_client(self):

        """
        Wait for a client connection.
        """

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

        """
        Stop the server and close all active connections.
        """

        self.close_client()
       
        if self.server:
            try:
                self.server.shutdown(socket.SHUT_RDWR)
            except OSError:
                #Socket may not be connected yet.
                pass

            try:
                self.server.close()
            finally:
                self.server = None


    def receive(self):
        """
        eceive a JSON message from the connected client.
        """
        return self.reader.readline().strip()
    
    def send(self, message):
        """
        Send a JSON message to the connected client.
        """

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
        """
        Close the active client connection.
        """
        
        if hasattr(self, "reader") and self.reader:
            try:
                self.reader.close()
            finally:
                self.reader = None

        if hasattr(self, "writer") and self.writer:
            try:
                self.writer.close()
            finally:
                self.writer = None

        if hasattr(self, "connection") and self.connection:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

            try:
                self.connection.close()
            finally:
                self.connection = None

        self.address = None

    def close(self):
        """
        Close the server socket.
        """
        
        self.close_client()

        if self.server:
            try:
                self.server.shutdown(socket.SHUT_RDWR)
            except OSError:
                #Socket may not be connected yet.
                pass

            try:
                self.server.close()
            finally:
                self.server = None