"""
camera_controller.py
"""
from pathlib import Path
from camera.mock_camera import MockCamera
from camera.pi_camera import PiCamera
from core.logger_manager import LoggerManager

class CameraController:
    def __init__(self):
        self.camera = None
        self.logger = None
        self.configuration = None

    def initialise(self, configuration, logger):
        self.configuration = configuration
        self.logger = logger

        #get camera driver from camera.json
        driver = configuration.get("camera","driver")
        

        if driver == "mock":

            self.camera = MockCamera(configuration)
            self.logger.warning(f"Mock Camera selected")

        elif driver == "pi":
            self.camera = PiCamera(configuration)
            self.logger.error(f"Pi Camera selected")
        else:
            self.logger.error(f"unknown camera driver: {driver}")
            raise ValueError(f"unknown camera driver: {driver}")

        self.camera.initialise(configuration,self.logger)

    def capture(self, filename: Path):
        return self.camera.capture_image(filename)
    def stop(self):
        self.camera.stop()

    def ready(self):
        return self.camera.is_ready()
    
    def get_state(self):

        return self.camera.get_state()
    
    def get_information(self):

        return self.camera.get_information()


    def get_status(self):

        return self.camera.get_status()
    
    def recover(self):

        self.camera.recover()