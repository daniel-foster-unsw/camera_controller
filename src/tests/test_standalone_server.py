
from src.communication.network_server import NetworkServer

server = NetworkServer()

server.initialise()

server.wait_for_client()

print("Connection successful")

server.stop()