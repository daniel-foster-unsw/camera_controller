"""
camera_exceptions.py

Custom exceptions for the Camera Controller.
"""

class CameraError(Exception):
    """Base camera exception."""
    pass


class CameraNotReadyError(CameraError):
    """Raised when capture is attempted before the camera is ready."""
    pass


class CameraInitialisationError(CameraError):
    """Raised when the camera fails to initialise."""
    pass


class CameraCaptureError(CameraError):
    """Raised when image capture fails."""
    pass


class CameraConfigurationError(CameraError):
    """Raised when the camera configuration is invalid."""
    pass

class CameraComponentNotImplementedError(CameraError):
    """Raised when a camera code component has not been implemented"""
    pass