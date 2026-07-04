"""
camera_controller.py
"""
from pathlib import Path
from camera.mock_camera import MockCamera

class CameraController:
    def __init__(self, configuration):
        self.camera = None

    def initialise(self, configuration):
        self.camera = MockCamera(configuration)
        self.camera.initialise()

    def capture(self, filename: Path):
        self.camera.capture_image(filename)

    def stop(self):
        self.camera.stop()

    def ready(self):
        return self.camera.is_ready()