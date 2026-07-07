"""
application.py 
Main application controller for the Core Scanner Camera Controller.
"""

from fileinput import filename
from multiprocessing.util import info
from typing import Self

from core.logger_manager import LoggerManager
from core.configuration import Configuration
from core.scan_controller import ScanController
from core.storage_exeptions import StorageSpaceError
from core.storage_manager import StorageManager
from camera.camera_controller import CameraController

from core.scan import Scan
from core.storage_exeptions import StoragePermissionError, StoragePathError

class Application:
    
    """
    Coordinates the startup, execution and shutdown of the Camera Controller application.
    """

    def __init__(self):
        #core services
        self.configuration = Configuration()
        self.logger = LoggerManager()
        #Core Models
        #self.storage = StorageManager()
        self.scan = Scan()
        #Managers
        self.storage = StorageManager(self.scan, self.configuration)
        self.camera = CameraController()

        self.scan_controller = ScanController(
            self.storage,
            self.camera,
            self.logger
        )

    def startup(self):
        
        
        print("Loading configuration...")
        try:
            self.configuration.load()

#            print("\nLoaded Settings:")
#            print(self.configuration.settings)

#            print("\nCamera Section:")
#            print(self.configuration.get("camera"))

#            print("\nCamera Width:")
#            print(self.configuration.get("camera", "width"))

        except Exception as e:
            print(f"Error loading configuration: {e}")
            raise

        #print("Starting logger...")
        #self.logger.start()

        self.logger.initialise(self.configuration)
#        self.logger.info("Application started.")

        print("Checking storage...")
        self.storage.initialise(self.scan, self.logger)

        self.camera.initialise(self.configuration,self.logger)
        #filename = self.storage.get_image_path()
        #self.camera.capture(filename)
        #print(f"Captured: {filename}")
        #print("\nCamera Controller Ready\n")
        self.logger.info("Camera Controller Ready.")

        self.scan_controller.initialise(
            self.configuration,
            self.logger
            )



        self.logger.info("Application started.")

    
    def run(self):

#        print("Application running...")
        self.logger.info("Application running.")
        
    def shutdown(self):

#        print("Shutting down...")
        self.logger.info("Shutting down...")


    #def capture_test_image(self):

    #    filename = self.storage.get_image_path()

    #    self.camera.capture(filename)

    #    print(f"Captured: {filename}")


    def capture_test_image(self):
        
        self.scan_controller.start_scan()
        try:
            self.scan_controller.capture_image()

        except StorageSpaceError:
            # Notify the operator that the drive is full
            self.logger.error(f"Not enough storage space: {e}")
            raise StorageSpaceError(
                f"Not enough storage space: {e}"
            )
            

        except StoragePermissionError: 
            # Tell the operator to check folder permissions
            self.logger.error(f"No permission for file path: {e}")
            raise StoragePermissionError(
                f"No permission for file path: {e}"
            )           
            

        except StoragePathError:
            # Ask the operator to verify the configured storage location 
            self.logger.error(f"Verify the configured storage location: {e}")
            raise StoragePathError(
                f"Verify the configured storage location: {e}"
            )
               
                
        self.scan_controller.stop_scan()

        #Test Code        
        info = self.camera.get_information()
        status = self.camera.get_status()
#        print(info)
#        print(status)

        print(f"Camera ID      : {info.camera_id}")
        print(f"Camera Name    : {info.camera_name}")
        print(f"Resolution     : {info.width} x {info.height}")
        print(f"Image Format   : {info.image_format}")
        print(f"Quality        : {info.quality}")

        print(f"State          : {status.state.name}")
        print(f"Ready          : {status.ready}")
        print(f"Connected      : {status.connected}")
        print(f"Initialised    : {status.initialised}")
        print(f"Capturing      : {status.capturing}")
        print(f"Error          : {status.error}")



        #Access Classes
    def show_camera_information(self):
        return self.camera.get_information()
    def show_camera_status(self):
        return self.camera.get_status()
    def show_storage_information(self):
        return self.storage.check_storage()
    def show_configuration(self):
         return self.configuration.settings
    def run_camera_self_test(self):
        return self.camera.self_test()
    def show_log_location(self):
        return self.logger.get_log_file()
        
    #get the system header
    def get_system_header(self):

        return {

            "camera_state":
                self.camera.get_state().name,

             "camera_driver":
                self.camera.get_information().camera_name,

            "camera_id":
                self.camera.get_information().camera_id,

            "storage":
                "READY",

            "images_taken":
                self.scan.image_number,

            "log_level":
                self.configuration.get(
                    "logging",
                    "level"
                ),

            "log_file":
               self.logger.get_log_file()

            }
        