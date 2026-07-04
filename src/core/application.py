"""
application.py 
Main application controller for the Core Scanner Camera Controller.
"""

from fileinput import filename

from core.logger_manager import LoggerManager
from core.configuration import Configuration
from core.storage_manager import StorageManager
from camera.camera_controller import CameraController
from core.scan import Scan

class Application:
    """
    Coordinates the startup, execution and shutdown of the Camera Controller application.
    """

    def __init__(self):
        self.logger = LoggerManager()
        self.configuration = Configuration()
        #self.storage = StorageManager()
        self.scan = Scan()
        self.storage = StorageManager(self.scan)
        self.camera = CameraController()

    def startup(self):
        

        print("Loading configuration...")
        try:
            self.configuration.load()
        except Exception as e:
            print(f"Error loading configuration: {e}")
            raise

        print("Starting logger...")
        self.logger.start()

        print("Checking storage...")
        self.storage.initialise()

        self.camera.initialise()
        filename = self.storage.get_image_path()

        self.camera.capture(filename)

        print(f"Captured: {filename}")


        print("\nCamera Controller Ready\n")

    def run(self):

        print("Application running...")

    def shutdown(self):

        print("Shutting down...")