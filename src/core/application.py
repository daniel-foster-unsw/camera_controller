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
        #self.storage = StorageManager()
        self.scan = Scan()
        self.storage = StorageManager(self.scan)
        self.camera = CameraController()
 #       self.serial_manager = SerialManager()
        self.communication = None
        self.command_parser = CommandParser(self, self.logger)

        self.image_transfer = ImageTransferService()

    def startup(self):
        

        print("Loading configuration...")
        try:
            self.configuration.load()

        except Exception as e:
            print(f"Error loading configuration: {e}")
            raise

        print("Starting logger...")
        self.logger.initialise(self.configuration)


#        print("Starting serial manager...")
#        self.serial_manager.initialise(self.configuration, self.logger)



        print("Starting communication manager...")
        mode = self.configuration.get(
            "communication",
            "mode"
        )

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

        self.communication.initialise(
            self.configuration,
            self.logger
        )

        print("Checking storage...")
  
        self.storage.initialise(self.configuration)

        self.camera.initialise(self.configuration, self.logger)
#        filename = self.storage.get_image_path()
#        self.camera.capture(filename)
#        print(f"Captured: {filename}")
        print("\nCamera Controller Ready\n")



        
    def run(self):
        """
        print("Application running...")
        while True:
            self.process_serial_command()
            
        """
        mode = self.configuration.get(
                "communication",
                "mode"
            )

        if mode == "menu":

            self.menu.run()

        else:

            self.communication_loop()
        
    def shutdown(self):

        print("Shutting down...")


#Menu Classes
    def capture_test_image(self):
        filename = self.storage.get_image_path()
        result = self.camera.capture(filename)
        #print(f"Captured: {filename}")
        return result


    def get_camera_information(self):
        return self.camera.get_information()
    
    def get_camera_status(self):
        return self.camera.get_status()
    
    def get_storage_information(self):
        return self.storage.check_storage()
    
    def get_configuration(self):
        return self.configuration.settings
    
    def run_camera_self_test(self):
        return self.camera.self_test()
    def get_system_header(self):
            return {
            "camera_state": self.camera.get_status().state.name,
            "camera_driver": self.configuration.get("camera", "driver"),
            "camera_id": self.camera.get_information().camera_id,
            "storage": str(self.storage.image_directory),
            "images_taken": self.scan.image_number,
            "log_level": self.configuration.get("logging", "level"),
            "log_file": str(self.logger.get_log_file()),
        }
           
    def show_log_location(self):
        return self.logger.get_log_file()
    
    def delete_image(self, filename: str) -> bool:
        """
        Delete an image.
        """

        return self.storage.delete_image(filename)

    def download_image(self, filename: str):
        """
        Load an image ready for transfer.
        """
        image_path = self.storage.find_image_path(filename)
        return self.image_transfer.load_image(image_path)
    
    def communication_loop(self):

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

                        self.communication.send(
                            JsonProtocol.serialize(header)
                        )

                        self.communication.send_bytes(response.data)
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


    
    """
    def process_serial_command(self):
        
 #       Process one incoming serial command.
        
        try:
            command = self.serial_manager.read()

            if command is None:
                return

            response = self.command_parser.execute(command)

            self.serial_manager.write(response)
        except Exception as error:

            self.logger.error(
                f"Serial communication error: {error}"
            )
    
    def communication_loop(self):

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

                json_response = JsonProtocol.serialize(response)
                self.logger.info(f"Sending: {json_response}")

                self.communication.send(json_response)
                

            except ConnectionResetError:
                self.logger.info("Client disconnected.")
                break

            except Exception as error:
                self.logger.error(error)
                break
"""

