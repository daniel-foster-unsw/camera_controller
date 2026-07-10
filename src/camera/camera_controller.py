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

        if driver is None:
            raise ValueError("Camera driver not specified in configuration.")
        

        if driver == "mock":

            self.camera = MockCamera(configuration)
            self.logger.info(f"Mock Camera selected")

        elif driver == "pi":
            self.camera = PiCamera(configuration)
            self.logger.info(f"Pi Camera selected")
        else:
            self.logger.error(f"unknown camera driver: {driver}")
            raise ValueError(f"unknown camera driver: {driver}")
        self.logger.info(f"Initialising {driver} camera driver...")
        self.camera.initialise(configuration,self.logger)
        self.logger.info(f"{driver.capitalize()} camera driver initialised successfully.")

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

    def self_test(self):
        """
        Run the camera driver's self test.
        """
        return self.camera.self_test()
    
    def get_driver(self):
        return type(self.camera).__name__