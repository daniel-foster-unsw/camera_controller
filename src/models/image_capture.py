from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class ImageCapture:
    filename: str
    path: Path
    timestamp: datetime
    camera_id: str
    width: int
    height: int
    success: bool