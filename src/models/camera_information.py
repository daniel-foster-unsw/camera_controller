"""
camera_information.py

Represents static camera information.
"""

from dataclasses import dataclass


@dataclass
class CameraInformation:

    camera_id: str

    camera_name: str

    width: int

    height: int

    image_format: str

    quality: int