"""
camera_interface.py

Abstract interface for camera implementations.
"""
from abc import ABC, abstractmethod
from pathlib import Path


class CameraInterface(ABC):
    @abstractmethod
    def initialise(self) -> None:
        """Initialise the camera."""
        pass

    @abstractmethod
    def capture_image(self, image_path: Path) -> None:
        """
        Capture an image and save it to the specified path.

        Args:
            image_path (Path): The path where the captured image will be saved.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the camera and release any resources."""
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """
        Check if the camera is ready for capturing images.

        Returns:
            bool: True if the camera is ready, False otherwise.
        """
        pass

    @abstractmethod
    def self_test(self):
        """Run the camera self-test."""
        pass


    @abstractmethod
    def get_information(self):
        """Return information about the camera."""
        pass

    @abstractmethod
    def get_status(self):
        """Return the current camera status."""
        pass

    @abstractmethod
    def get_state(self):
        """Return the current camera state."""
        pass

    @abstractmethod
    def recover(self):
        """Attempt to recover the camera from an error state."""
        pass