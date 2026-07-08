from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from communication.response import Response
from communication.command import Command
from communication.serial_manager import SerialManager
from communication.command_parser import CommandParser
from core.application import Application
from core.logger_manager import LoggerManager




class DummyApplication:
    def get_camera_status(self):
        return {
            "state": "READY",
            "connected": True,
            "initialised": True,
            "capturing": False,
            "error": False
        }

    def get_camera_information(self):
        return {
            "camera_id": "CAM01",
            "camera_name": "Mock Camera"
        }

    def get_storage_information(self):
        return {
            "directory": "images/",
            "free_space": "10 GB"
        }

    def get_configuration(self):
        return {
            "driver": "mock"
        }

    def run_camera_self_test(self):
        return True

    def capture_test_image(self):
        return "DummyApplication File Address"
    pass
class DummyLogger:
    pass

logger = DummyLogger()
application = DummyApplication()
parser = CommandParser(application, logger)

commands = [

    '{"version":"1.0","command":"INVALID"}',
    '{"version":"2.0","command":"PING"}',
    '{"version":"1.0","command":"PING"}',
    '{"version":"1.0","command":"GET_CAMERA_STATUS"}',
    '{"version":"1.0","command":"GET_CAMERA_INFORMATION"}',
    '{"version":"1.0","command":"GET_STORAGE_INFORMATION"}',
    '{"version":"1.0","command":"GET_CONFIGURATION"}',
    '{"version":"1.0","command":"SELF_TEST"}',
    '{"version":"1.0","command":"CAPTURE_IMAGE"}'


]

for message in commands:

    print("=" * 60)

    command = Command.from_json(message)

    print("Incoming Command")

    print(command)

    response = parser.execute(command)

    print()

    print("Outgoing Response")

    print(response)

    print()

    print(response.to_json())

    print()






"""
#Test Invalid Command
command = Command.from_json(
#    '{"version":"1.0","command":"PING"}'
    '{"version":"1.0","command":"INVALID"}'
)
response = parser.execute(command)
print("Incoming Command")
print(command)
print()
print("Outgoing Response")
print(response)
print()
print("JSON Returned")
print(response.to_json())

#Test PING Command
command = Command.from_json(
    '{"version":"1.0","command":"PING"}'
)
response = parser.execute(command)
print("Incoming Command")
print(command)
print()
print("Outgoing Response")
print(response)
print()
print("JSON Returned")
print(response.to_json())

#Test GET_CAMERA_STATUS Command
command = Command.from_json(
    '{"version":"1.0","command":"GET_CAMERA_STATUS"}'
)
response = parser.execute(command)
print("Incoming Command")
print(command)
print()
print("Outgoing Response")
print(response)
print()
print("JSON Returned")
print(response.to_json())

#Test GET_CAMERA_INFORMATION Command
command = Command.from_json(
    '{"version":"1.0","command":"GET_CAMERA_INFORMATION"}'
)
response = parser.execute(command)
print("Incoming Command")
print(command)
print()
print("Outgoing Response")
print(response)
print()
print("JSON Returned")
print(response.to_json())

#Test GET_STORAGE_INFORMATION Command
command = Command.from_json(
    '{"version":"1.0","command":"GET_STORAGE_INFORMATION"}'
)
response = parser.execute(command)
print("Incoming Command")
print(command)
print()
print("Outgoing Response")
print(response)
print()
print("JSON Returned")
print(response.to_json())


#Test GET_CONFIGURATION Command
command = Command.from_json(
    '{"version":"1.0","command":"GET_CONFIGURATION"}'
)
response = parser.execute(command)
print("Incoming Command")
print(command)
print()
print("Outgoing Response")
print(response)
print()
print("JSON Returned")
print(response.to_json())


#Test SELF_TEST Command
command = Command.from_json(
    '{"version":"1.0","command":"SELF_TEST"}'
)
response = parser.execute(command)
print("Incoming Command")
print(command)
print()
print("Outgoing Response")
print(response)
print()
print("JSON Returned")
print(response.to_json())


#Test CAPTURE_IMAGE Command
command = Command.from_json(
    '{"version":"1.0","command":"CAPTURE_IMAGE"}'
)
response = parser.execute(command)
print("Incoming Command")
print(command)
print()
print("Outgoing Response")
print(response)
print()
print("JSON Returned")
print(response.to_json())
"""