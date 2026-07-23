"""
application.py 
Main application controller for the Core Scanner Camera Controller.
"""

from core.logger_manager import LoggerManager
from core.configuration import Configuration
from core.storage_manager import StorageManager
from camera.camera_controller import CameraController

from communication.response import Response

from communication.serial_manager import SerialManager
from communication.command_parser import CommandParser
from communication.network_server import NetworkServer

from communication.json_protocol import JsonProtocol
from services.image_transfer_service import ImageTransferService

from models.image_transfer import ImageTransfer

class Application:
    """
    Coordinates the startup, execution and shutdown of the Camera Controller application.
    """

    def __init__(self):
        self.logger = LoggerManager()
        self.configuration = Configuration()
        
        self.storage = StorageManager()
        self.camera = CameraController()

        self.communication = None
        self.command_parser = CommandParser(self, self.logger)

        self.image_transfer = ImageTransferService()

    def startup(self):
        """initalise the camera controller"""
        try:
            print("Loading configuration...")
            try:
                self.configuration.load()

            except Exception as e:
                print(f"Error loading configuration: {e}")
                raise

            print("Starting logger...")
            self.logger.initialise(self.configuration)

            print("Starting communication manager...")
            mode = self.configuration.get("communication", "mode")

            if mode == "serial":

                print("Starting serial manager...")

                self.communication = SerialManager()

            elif mode == "network":

                print("Starting network server...")

                network = self.configuration.get("communication", "network")

                self.communication = NetworkServer(
                    host=network["host"],
                    port=network["port"]
                )

            else:

                raise ValueError(
                    f"Unknown communication mode: {mode}"
                )

            self.communication.initialise(self.configuration, self.logger)

            print("Checking storage...")
            self.storage.initialise(self.configuration, self.logger)

            print("Checking camera...")
            self.camera.initialise(self.configuration, self.logger)
            print("\nCamera Controller Ready\n")
            
        except Exception:
            self.shutdown()
            raise



        
    def run(self):
        """run the camera controller"""
        mode = self.configuration.get(
                "communication",
                "mode"
            )

        if mode == "menu":

            self.menu.run()

        else:

            self.communication_loop()
        
    def shutdown(self):
        """ shut down the camera controller"""
        self.logger.info("Shutting down Camera Controller...")
        try:
            if self.communication is not None:
                self.communication.stop()
        except Exception as ex:
            self.logger.error(f"Error stopping communication: {ex}")

        try:
            if self.camera:
                self.camera.stop()
        except Exception as ex:
            self.logger.error(f"Error shutting down camera: {ex}")

        self.logger.info("Application shutdown complete.")


#Menu Classes
    def capture_image(self):
        """capture an image on the selected camera"""
        filename = self.storage.get_image_path()
        result = self.camera.capture(filename)
        return result


    def get_camera_information(self):
        """get all camera information"""
        return self.camera.get_information()
    
    def get_camera_status(self):
        """get the status of the camera"""
        return self.camera.get_status()
    
    def get_storage_information(self):
        """check storage drive"""
        return self.storage.check_storage()
    
    def get_configuration(self):
        """get information from config file"""
        return self.configuration.settings
    
    def run_camera_self_test(self):
        """run self test on the selected camera"""
        return self.camera.self_test()
    
    def get_system_header(self):
        """get system informaion"""
        images_taken = 0

        if self.storage.scan is not None:
            images_taken = self.storage.scan.image_number
    
        return {
            "camera_state": self.camera.get_status().state.name,
            "camera_driver": self.configuration.get("camera", "driver"),
            "camera_id": self.camera.get_information().camera_id,
            "storage": str(self.storage.image_directory),
            "images_taken": images_taken,
            "log_level": self.configuration.get("logging", "level"),
            "log_file": str(self.logger.get_log_file()),
        }
           
    def get_log_location(self):
        """provide the location of the log file"""
        return self.logger.get_log_file()
       
    def download_image(self, filename: str):
        """
        Load an image ready for transfer.
        """
        image_path = self.storage.find_image_path(filename)
        return self.image_transfer.load_image(image_path)
    
    def delete_image(self, filename: str) -> bool:
        """
        Delete an image.
        """

        return self.storage.delete_image(filename)

    def list_images(self):
        """
        Return all stored scans.
        """
        return self.storage.list_images()

    def delete_scan(self, scan: str):
        """delete scan directory"""
        return self.storage.delete_scan(scan)

    def start_scan(self):
        """start new scan"""
        return self.storage.start_scan()

    def stop_scan(self):
        """end current scan"""
        return self.storage.stop_scan()

    def get_scan(self):
        """Getr scan id"""
        return self.storage.get_scan()


    def communication_loop(self):
        """ primary code loop for code exicution """
        while True:

            self.communication.wait_for_client()

            self.logger.info("Communication client connected.")

            while True:

                try:

                    message = self.communication.receive()

                    if message == "":
                        self.logger.info("Client disconnected.")
                        break

                    self.logger.info(f"Received: {message}")

                    command = JsonProtocol.deserialize(message)

                    response = self.command_parser.execute(command)
 
                    if isinstance(response, ImageTransfer):

                        header = Response(
                            version="1.0",
                            status="OK",
                            message="Image transfer starting.",
                            data={
                                "filename": response.filename,
                                "filesize": response.filesize
                            }
                        )

                        #Sending Header
                        json_header = JsonProtocol.serialize(header)
                        self.logger.info(f"Sending header: {json_header}")
                        self.communication.send(json_header)
                        #Sending data
                        self.logger.info(f"Sending {response.filesize} bytes...")
                        self.communication.send_bytes(response.data)
                        self.logger.info("Image transfer complete.")

                        continue

                        
                    else:
                        json_response = JsonProtocol.serialize(response)
                        self.logger.info(f"Sending: {json_response}")
                        self.communication.send(json_response)

                except ConnectionResetError:
                    self.logger.info("Client disconnected.")
                    break

                except Exception as error:
                    self.logger.error(error)
                    break

            # Clean up the old client connection
            self.communication.close_client()
 

