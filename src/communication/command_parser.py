"""
command_parser.py

Parses commands received over USB.
"""
from communication.json_protocol import JsonProtocol
from communication.protocol import (
    PROTOCOL_VERSION,
    PING,
    STATUS_OK,
    STATUS_ERROR,
    CAPTURE_IMAGE,
    GET_CAMERA_INFORMATION,
    GET_CAMERA_STATUS,
    GET_STORAGE_INFORMATION,
    GET_CONFIGURATION,
    SELF_TEST,
    SHUTDOWN,
    DOWNLOAD_IMAGE,
    DELETE_IMAGE,
    LIST_IMAGES,
    DELETE_SCAN
)

from .response import Response

class CommandParser:

    def __init__(self, application, logger):

        self.application = application
        self.logger = logger

    def execute(self, command):

        if command.version != PROTOCOL_VERSION:
            return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_ERROR,
            message=f"Unknown protocol version: {command.version}"
        )



        elif command.command == PING:
            return Response(
                version=PROTOCOL_VERSION,
                status=STATUS_OK,
                message="PONG"
            )
        
        elif command.command == GET_CAMERA_STATUS:
            return self._handle_camera_status()

        elif command.command == GET_CAMERA_INFORMATION:
            return self._handle_camera_information()

        elif command.command == GET_STORAGE_INFORMATION:
            return self._handle_storage_information()

        elif command.command == GET_CONFIGURATION:
            return self._handle_configuration()

        elif command.command == SELF_TEST:
            return self._handle_self_test()

        elif command.command == CAPTURE_IMAGE:
            return self._handle_capture_image()
        
        elif command.command == DOWNLOAD_IMAGE:
            return self._handle_download_image(command)
#            filename = command.parameters["filename"]
#            image = self.application.download_image(filename)
#            return image

        elif command.command == DELETE_IMAGE:
            return self._handle_delete_image(command)
        
        elif command.command == LIST_IMAGES:
            return self._handle_list_images(command)
        
        elif command.command == DELETE_SCAN:
            return self._handle_delete_scan(command)

            



        else:        
            return Response(
                version=PROTOCOL_VERSION,
                status=STATUS_ERROR,
                message=f"Unknown command: {command.command}"
            )

        raise ValueError(
            f"Unknown command: {command.command}"
        )
    
    def _handle_camera_status(self):

        status = self.application.get_camera_status()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Camera status.",
            data=status.to_dict()
        )
    
    def _handle_camera_information(self):

        information = self.application.get_camera_information()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Camera information.",
            data=information
        )
    
    def _handle_storage_information(self):

        storage = self.application.get_storage_information()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Storage information.",
            data=storage
        )
    
    def _handle_configuration(self):

        configuration = self.application.get_configuration()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Configuration.",
            data=configuration
        )
    
    def _handle_self_test(self):

        result = self.application.run_camera_self_test()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Self test complete.",
            data=result
        )
    

    def _handle_capture_image(self):

        result = self.application.capture_image()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Image captured.",
            data={
                "filename": str(result.filename),
                "filesize": result.filesize,
#                "filesize": str(result.filesize),
                "width": result.width,
                "height": result.height,
                "format":result.image_format
            }
        )
    
    def _handle_download_image(self, command):
        try:
            filename = command.parameters["filename"]
            image = self.application.download_image(filename)
            return image
        
        except FileNotFoundError:
            return Response(version = "1.0", status="ERROR", message="Image not found.")
        

    def _handle_delete_image(self, command):

        filename = command.parameters["filename"]

        deleted = self.application.delete_image(filename)

        if deleted:

            return Response(
                version=PROTOCOL_VERSION,
                status=STATUS_OK,
                message="Image deleted."
            )

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_ERROR,
            message="Image not found."
        )
    
    def _handle_list_images(self, command):

        scans = self.application.list_images()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Images found.",
            data={
                "scans": scans
            }
        )
    
    def _handle_delete_scan(self, command):

        scan = command.parameters["scan"]

        deleted = self.application.delete_scan(scan)

        if deleted:
            return Response(
                version=PROTOCOL_VERSION,
                status=STATUS_OK,
                message="Scan deleted."
            )

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_ERROR,
            message="Scan not found."
        )