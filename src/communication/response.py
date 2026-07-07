"""
response.py

Represents a response returned to the PC.
"""
from dataclasses import dataclass

@dataclass
class Response:

    version: str

    status: str

    message: str

    data: dict | None = None