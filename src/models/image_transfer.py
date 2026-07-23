"""
image_transfer.py

Represents an image prepared for transfer to a remote client.
"""

from dataclasses import dataclass

@dataclass
class ImageTransfer:
    """Stores image metadata and binary data for transfer."""
    filename: str
    filesize: int
    data: bytes