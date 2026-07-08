
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from communication.response import Response
from communication.command import Command
from communication.serial_manager import SerialManager
from communication.command_parser import CommandParser
from core.application import Application
app = Application()
app.startup()

parser = CommandParser(app)



command = Command.from_json(
    '{"version":"1.0","command":"PING"}'
)

response = parser.execute(command)

print(response.to_json())

app.shutdown()