from dataclasses import dataclass

@dataclass
class ImageTransfer:
    filename: str
    filesize: int
    data: bytes