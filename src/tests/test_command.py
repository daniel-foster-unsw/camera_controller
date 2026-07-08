from pathlib import Path
import sys

# Add the src directory to Python's search path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from communication.command import Command

json_message = '{"version":"1.0","command":"PING"}'

command = Command.from_json(json_message)

print(command)