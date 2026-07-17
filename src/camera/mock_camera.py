"""
mock_camera.py

Simulated camera for Windows development.
"""
#from email.mime import image
#from fileinput import filename
from datetime import datetime
from email.mime import image
from fileinput import filename
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from camera.camera_exceptions import CameraConfigurationError, CameraNotReadyError
from core.configuration import Configuration
from datetime import datetime
from models.capture_result import CaptureResult
from models.camera_information import CameraInformation
from models.camera_status import CameraStatus
from camera.camera_state import CameraState
from camera.camera_exceptions import CameraCaptureError
from core.storage_exceptions import StoragePermissionError, StorageWriteError



from camera.camera_interface import CameraInterface
from models.capture_result import CaptureResult

class MockCamera(CameraInterface):
    def __init__(self, configuration):
        """
        Initialise the mock camera.
        """
        self.logger = None
#        self.ready = False
        self.configuration = configuration
        self.camera_id = configuration.get("camera", "id")
        self.width = configuration.get("camera", "width")
        self.height = configuration.get("camera", "height")
        self.image_format = configuration.get("camera", "format")
        self.state = CameraState.UNINITIALISED







    def initialise(self,configuration, logger) -> None:
        """
        Initialise the mock camera.
        """
#        print(self.camera_id)
#        print(self.width)
#        print(self.height)
#        print(self.image_format)
        self.logger = logger
        self.state = CameraState.INITIALISING

        #Validate Configuration
        if self.width <= 0:
            self.logger.error("Invalid camera width.")
            raise CameraConfigurationError(
                "Invalid camera width."
            )

        if self.height <= 0:
            self.logger.error("Invalid camera height.")
            raise CameraConfigurationError(
                "Invalid camera height."
            )

        if not self.camera_id:
            self.logger.error("Camera ID not configured.")
            raise CameraConfigurationError(
                "Camera ID not configured."
            )






        # Read configuration
        # Prepare camera
#        self.ready = True
        self.state = CameraState.READY
        #print("✓ Mock Camera Ready")
        self.logger.info("Mock camera initialised.")
        

    def capture_image(self, filename: Path):
        """
        Simulate capturing an image and saving it to the specified path.

        Args:
            image_path (Path): The path where the captured image will be saved.
        """
        if self.state != CameraState.READY:
            self.logger.error("Camera is not ready for image capture.")
            raise CameraNotReadyError(
                "Camera is not ready for image capture."
            )
        
        self.state = CameraState.CAPTURING
        #print(f"capturing image -> {filename}")
        self.logger.info(f"Capturing image: {filename.name}")
        image = Image.new(
        "RGB",
        (self.width, self.height),
        "white"
        )

        draw = ImageDraw.Draw(image)

        # Try to use a larger TrueType font
        try:
            title_font = ImageFont.truetype("arial.ttf", 80)
            body_font = ImageFont.truetype("arial.ttf", 50)
        except OSError:
            self.state = CameraState.ERROR
            # Fall back if Arial isn't available
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()

        # Draw a border
        margin = 50
        draw.rectangle(
            (margin, margin, self.width - margin, self.height - margin),
            outline="black",
            width=8
        )

        # Title
        draw.text(
            (150, 150),
            "Core Scanner Camera Controller",
            fill="black",
            font=title_font
        )

        # Subtitle
        draw.text(
            (150, 280),
            "MOCK CAMERA IMAGE",
            fill="black",
            font=body_font
        )

        # Camera information
        y = 450
        line_spacing = 80

        draw.text((150, y), f"Camera ID : {self.camera_id}", fill="black", font=body_font)
        y += line_spacing

        draw.text((150, y), f"Resolution : {self.width} x {self.height}", fill="black", font=body_font)
        y += line_spacing

        draw.text((150, y), f"Filename : {filename.name}", fill="black", font=body_font)

        try:

            image.save(filename)
            filesize = filename.stat().st_size
            self.state = CameraState.READY
#            print("Save succeeded")
            self.logger.info(f"Image saved: {filename}")

        except PermissionError as e:
            self.logger.error(f"Unable to write image: {e}")
            raise StoragePermissionError(
                "Cannot write image to storage."
            ) from e

        except OSError as e:

            self.state = CameraState.ERROR
            self.logger.error(f"Image write failed: {e}")
            raise StorageWriteError("Failed to write image to storage.") from e
#        print(f"✓ Image saved -> {filename}")
#        self.logger.info(f"Image saved: {filename}")
    
        return CaptureResult(

                success=True,

                filename=filename.name,

                path=filename,

                timestamp=datetime.now(),

                width=self.width,

                height=self.height,

                camera_id=self.camera_id,

                image_format=self.image_format,
                filesize=filesize

        )













    def stop(self):
        """
        Stop the mock camera.
        """
#        self.ready = False
        self.state = CameraState.SHUTDOWN
#        print("Camera stopped")
        self.logger.info("Mock camera stopped.")

    def is_ready(self):
        """
        Check if the mock camera is ready for capturing images.

        Returns:
            bool: Always returns True for the mock camera.
        """
        return self.state == CameraState.READY
    
    def get_state(self):

        return self.state
    
    def get_information(self):

        return CameraInformation(

            camera_id=self.camera_id,

            camera_name="Mock Camera",

            width=self.width,

            height=self.height,

            image_format=self.image_format,

            quality=self.configuration.get(
                "camera",
                "quality"
            )
        )
    

    def get_status(self):

            return CameraStatus(

            state=self.state,

            ready=self.state == CameraState.READY,

            connected=True,

            initialised=self.state != CameraState.UNINITIALISED,

            capturing=self.state == CameraState.CAPTURING,

            error=self.state == CameraState.ERROR

        )
    
    def self_test(self):

        tests = []

        tests.append(self.width > 0)

        tests.append(self.height > 0)

        tests.append(self.camera_id is not None)

        tests.append(self.image_format is not None)

        return all(tests)
    

    def recover(self):

        self.logger.warning(
            "Attempting camera recovery."
        )

        self.state = CameraState.INITIALISING

        self.initialise(self.logger)