from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from communication.response import Response

response = Response(
    version="1.0",
    status="OK",
    message="PONG"
)

print(response)

print()

print(response.to_json())