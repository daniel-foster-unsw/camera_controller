"""
image_capture.py

Represents the result of an image capture operation.
"""
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class ImageCapture:
    """Stores metadata describing a captured image."""
    filename: str
    path: Path
    timestamp: datetime
    camera_id: str
    width: int
    height: int
    success: bool