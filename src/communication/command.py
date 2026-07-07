"""
command.py

Represents a command received over USB.
"""

from dataclasses import dataclass

@dataclass
class Command:

    version: str

    command: str

    parameters: dict | None = None