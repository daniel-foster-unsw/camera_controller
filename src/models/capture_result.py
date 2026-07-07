"""
capture_result.py

Represents the result of a camera capture.
"""

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass
class CaptureResult:

    success: bool

    filename: str

    path: Path

    timestamp: datetime

    width: int

    height: int

    camera_id: str

    image_format: str