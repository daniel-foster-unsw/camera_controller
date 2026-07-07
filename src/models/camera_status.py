"""
camera_status.py

Represents the current operating status of the camera.
"""

from dataclasses import dataclass
from camera.camera_state import CameraState


@dataclass
class CameraStatus:

    state: CameraState

    ready: bool

    connected: bool

    initialised: bool

    capturing: bool

    error: bool