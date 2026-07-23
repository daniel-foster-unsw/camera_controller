"""
command_parser.py

Parses commands received over USB.
"""



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
    DELETE_SCAN,
    START_SCAN,
    STOP_SCAN,
    GET_SCAN
)

from .response import Response
from core.storage_exceptions import StorageError

class CommandParser:

    def __init__(self, application, logger):

        self.application = application
        self.logger = logger

    def execute(self, command):
        """
        Execute a protocol command.
        """

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


        elif command.command == DELETE_IMAGE:
            return self._handle_delete_image(command)
        
        elif command.command == LIST_IMAGES:
            return self._handle_list_images(command)
        
        elif command.command == DELETE_SCAN:
            return self._handle_delete_scan(command)
        
        elif command.command == START_SCAN:
            return self._handle_start_scan()
        
        elif command.command == STOP_SCAN:
            return self._handle_stop_scan()
        
        elif command.command == GET_SCAN:
            return self._handle_get_scan()

            



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
        """
        handle camera status command
        """
        status = self.application.get_camera_status()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Camera status.",
            data=status.to_dict()
        )
    
    def _handle_camera_information(self):
        """
        handle camera information command
        """
        information = self.application.get_camera_information()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Camera information.",
            data=information
        )
    
    def _handle_storage_information(self):
        """
        handle storage information command
        """
        storage = self.application.get_storage_information()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Storage information.",
            data=storage
        )
    
    def _handle_configuration(self):
        """
        handle configuration command
        """
        configuration = self.application.get_configuration()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Configuration.",
            data=configuration
        )
    
    def _handle_self_test(self):
        """
        handle self test command command
        """

        result = self.application.run_camera_self_test()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Self test complete.",
            data=result
        )
    

    def _handle_capture_image(self):
        """
        handle capture image command
        """

        self.application.storage.require_scan()
        

        result = self.application.capture_image()

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Image captured.",
            data={
                "filename": str(result.filename),
                "filesize": result.filesize,
                "width": result.width,
                "height": result.height,
                "format":result.image_format
            }
        )
    
    def _handle_download_image(self, command):
        """
        handle download image command command
        """
        try:


            filename = command.parameters["filename"]
            image = self.application.download_image(filename)
            return image
        
        except FileNotFoundError:
            return Response(version = "1.0", status="ERROR", message="Image not found.")
        

    def _handle_delete_image(self, command):
        """
        handle delete image command command
        """

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
        """
        handle list images command
        """
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
    
    def _handle_start_scan(self):
        """
        handle start scan command
        """
        scan = self.application.start_scan()
        
        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Scan started.",
            data=scan
        )
    
    def _handle_stop_scan(self):
        """
        handle stop scan command
        """
        try:

            scan = self.application.stop_scan()

            return Response(
                version=PROTOCOL_VERSION,
                status=STATUS_OK,
                message="Scan stopped.",
                data=scan
            )
        except StorageError:
            return Response(
                version=PROTOCOL_VERSION,
                status=STATUS_ERROR,
                message="No active scan."
            )

    
    def _handle_get_scan(self):
        """
        handle handle get scan id command
        """
        scan = self.application.get_scan()

        if scan is None:
            return Response(
                version=PROTOCOL_VERSION,
                status=STATUS_OK,
                message="No active scan.",
                data=None
            )

        return Response(
            version=PROTOCOL_VERSION,
            status=STATUS_OK,
            message="Current scan.",
            data=scan
        )