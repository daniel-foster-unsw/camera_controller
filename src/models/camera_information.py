"""
camera_information.py

Represents static camera information.
"""

from dataclasses import dataclass


@dataclass
class CameraInformation:
    """Stores static information about a camera."""

    camera_id: str

    camera_name: str

    width: int

    height: int

    image_format: str

    quality: int