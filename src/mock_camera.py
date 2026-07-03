"""
mock_camera.py

Simulated camera for Windows development.
"""
from pathlib import Path
from interfaces.camera_interface import CameraInterface

class MockCamera(CameraInterface):
    def __init__(self):
        """
        Initialise the mock camera.
        """
        self.ready = False

    def initialise(self) -> None:
        """
        Initialise the mock camera.
        """
        print("Mock camera initialised.")
        self.ready = True

    def capture_image(self, filename: Path) -> None:
        """
        Simulate capturing an image and saving it to the specified path.

        Args:
            image_path (Path): The path where the captured image will be saved.
        """
        
        print(f"capturing image -> {filename}")
        filename.touch()  # Create an empty file to simulate image capture

    def stop(self):
        """
        Stop the mock camera.
        """
        print("Camera stopped")

    def is_ready(self):
        """
        Check if the mock camera is ready for capturing images.

        Returns:
            bool: Always returns True for the mock camera.
        """
        return self.ready