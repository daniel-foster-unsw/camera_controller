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


    def to_dict(self):
        return {
            "state": self.state.name,
            "ready": self.ready,
            "connected": self.connected,
            "initialised": self.initialised,
            "capturing": self.capturing,
            "error": self.error
        }