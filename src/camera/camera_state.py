"""
camera_state.py

Defines the operational states of the camera.
"""

from enum import Enum


class CameraState(Enum):

    UNINITIALISED = 0

    INITIALISING = 1

    READY = 2

    CAPTURING = 3

    ERROR = 4

    SHUTDOWN = 5