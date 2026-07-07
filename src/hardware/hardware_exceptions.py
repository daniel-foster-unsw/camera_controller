"""
camera_exceptions.py

Custom exceptions for the Camera Controller.
"""

class HarwareError(Exception):
    """Base camera exception."""
    pass


class HarwareNotReadyError(CameraError):
    """Raised when capture is attempted before the camera is ready."""
    pass


class HarwareInitialisationError(CameraError):
    """Raised when the camera fails to initialise."""
    pass


class HarwareCaptureError(CameraError):
    """Raised when image capture fails."""
    pass


class HarwareConfigurationError(CameraError):
    """Raised when the camera configuration is invalid."""
    pass