"""
camera_controller.py
"""
from pathlib import Path
from camera.mock_camera import MockCamera

class CameraController:
    def __init__(self):
        self.camera = MockCamera()

    def initialise(self):
        self.camera.initialise()

    def capture(self, filename: Path):
        self.camera.capture_image(filename)

    def stop(self):
        self.camera.stop()

    def ready(self):
        return self.camera.is_ready()