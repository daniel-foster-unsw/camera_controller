"""
communication_interface.py

Abstract interface for all Camera Controller communication transports.
"""

from abc import ABC, abstractmethod


class CommunicationInterface(ABC):

    @abstractmethod
    def initialise(self, configuration, logger):
        """Initialise the communication transport."""
        pass

    def wait_for_client(self):
        """
        Optional for communication transports that require a client connection.
        """
        return

    @abstractmethod
    def receive(self):
        """Receive a message from the client."""
        pass

    @abstractmethod
    def send(self, message):
        """Send a message to the client."""
        pass

    @abstractmethod
    def stop(self):
        """Close the communication transport."""
        pass

    @abstractmethod
    def send_bytes(self, data: bytes):
        """Send binary data."""
        pass