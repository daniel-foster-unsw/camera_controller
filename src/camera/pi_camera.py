"""
pi_camera.py

Camera implementation for the Raspberry Pi Camera Module.
"""

from pathlib import Path

from camera.camera_interface import CameraInterface
from datetime import datetime

from camera.camera_exceptions import CameraNotReadyError, CameraCaptureError, CameraComponentNotImplementedError
from camera.camera_state import CameraState

from core.logger_manager import logging

from models.camera_information import CameraInformation
from models.camera_status import CameraStatus
from models.capture_result import CaptureResult



from time import sleep

class PiCamera(CameraInterface):

    def __init__(self, configuration):

        self.configuration = configuration
        self.logger = None
        self.camera = None

        self.camera_id = None
        self.width = None
        self.height = None
        self.image_format = None

        self.state = CameraState.UNINITIALISED

    def initialise(self, configuration, logger):
        from picamera2 import Picamera2

        try:
            self.state = CameraState.INITIALISING
            self.logger = logger
            self.configuration = configuration

            #read configuration
            self.camera_id = configuration.get("camera", "id")
            self.width = configuration.get("camera", "width")
            self.height = configuration.get("camera", "height")
            self.image_format = configuration.get("camera", "format")
            self.logger.info(f"Camera resolution: {self.width} x {self.height}")
            self.logger.info(f"Image format: {self.image_format}")


            self.camera = Picamera2()
            capture_config = self.camera.create_still_configuration(main={"size":(self.width, self.height)})

            self.camera.configure(capture_config)
            self.camera.start()
            sleep(configuration.get("camera","warmup_time"))
            self.state = CameraState.READY

            self.logger.info("pi Camera initialised.")
        except Exception as e:
            self.state = CameraState.ERROR
            self.logger.error(
                f"Failed to initialise Pi Camera: {e}"
            )
            raise


    def capture_image(self, filename):

        if self.state != CameraState.READY:
            raise CameraNotReadyError("Camera is not Ready")
            
        self.state = CameraState.CAPTURING

        try:
            self.logger.info(f"Capturing image: {filename.name}")

            # Actual pi camera capture
            filename.parent.mkdir(
            parents=True,
            exist_ok=True
            )

            self.camera.capture_file(str(filename))
            self.state = CameraState.READY
            self.logger.info(f"Image saved: {filename}")

            return CaptureResult(success=True,
                filename=filename.name,
                path=filename,
                timestamp=datetime.now(),
                width=self.width,
                height=self.height,
                camera_id=self.camera_id,
                image_format=self.image_format
            )
        except Exception as e:
            self.state = CameraState.ERROR
            self.logger.error(f"Capture failed: {e}")
            raise CameraCaptureError(str(e))
            

    def stop(self):
        """
        Stop Pi Camera.
        """
        if self.camera is not None:
            self.camera.stop()
            self.camera.close()
            self.camera = None
        self.state = CameraState.SHUTDOWN
        self.logger.info("Pi Camera stopped.")
#        raise CameraComponentNotImplementedError("code component Stop() in pi_camera not implemented")



    def is_ready(self):
        """
        Check if the mock camera is ready for capturing images.

        Returns:
            bool: Always returns True for the mock camera.
        """
#        self.logger.error("code component is_ready() in pi_camera not implemented")
#        raise CameraComponentNotImplementedError("code component is_ready() in pi_camera not implemented")
        return self.state == CameraState.READY
    
    def get_state(self):
 #       self.logger.error("code component get_state() in pi_camera not implemented")
#      raise CameraComponentNotImplementedError("code component get_state() in pi_camera not implemented")

        return self.state
    
    def get_information(self):

        return CameraInformation(

            camera_id=self.camera_id,

            camera_name="Raspberry Pi Camera Module 3",

            width=self.width,

            height=self.height,

            image_format=self.image_format,

            quality=self.configuration.get(
                "camera",
                "quality"
            )
        )
    

    def get_status(self):
            
#        self.logger.error("code component get_status() in pi_camera not implemented")
#        raise CameraComponentNotImplementedError("code component get_status() in pi_camera not implemented")

        return CameraStatus(

            state=self.state,

            ready=self.state == CameraState.READY,

            connected=self.camera is not None,

            initialised=self.state != CameraState.UNINITIALISED,

            capturing=self.state == CameraState.CAPTURING,

            error=self.state == CameraState.ERROR

        )
    
    def self_test(self):

        tests = []
        tests.append(self.camera is not None)

        tests.append(self.width > 0)

        tests.append(self.height > 0)

        tests.append(self.camera_id is not None)

        tests.append(self.image_format is not None)

        tests.append(self.state == CameraState.READY)

        return all(tests)
    

    def recover(self):

        self.logger.warning(
            "Attempting camera recovery."
        )
#        self.logger.error("code component recover() in pi_camera not implemented")
#        raise CameraComponentNotImplementedError("code component recover() in pi_camera not implemented")
        try:
            self.stop()
            self.camera.close()
            self.camera = None
            self.state = CameraState.SHUTDOWN
        

            self.state = CameraState.INITIALISING
            self.initialise(self.configuration,self.logger)
            self.state = CameraState.READY

        except Exception:
            self.logger.error(f"Camera recovery failed: {e}")
            self.state = CameraState.ERROR
            pass
        return self.is_ready()

        