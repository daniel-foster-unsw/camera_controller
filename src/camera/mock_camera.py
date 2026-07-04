"""
mock_camera.py

Simulated camera for Windows development.
"""
#from email.mime import image
#from fileinput import filename
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from core.configuration import Configuration



from camera.camera_interface import CameraInterface

class MockCamera(CameraInterface):
    def __init__(self, configuration):
        """
        Initialise the mock camera.
        """
        self.ready = False
        self.configuration = configuration
        self.camera_id = configuration.get("camera", "id")
        self.width = configuration.get("camera", "width")
        self.height = configuration.get("camera", "height")
        self.image_format = configuration.get("camera", "format")







    def initialise(self) -> None:
        """
        Initialise the mock camera.
        """
        print(self.camera_id)
        print(self.width)
        print(self.height)
        print(self.image_format)

        self.ready = True
        print("✓ Mock Camera Ready")
        

    def capture_image(self, filename: Path):
        """
        Simulate capturing an image and saving it to the specified path.

        Args:
            image_path (Path): The path where the captured image will be saved.
        """
        
        print(f"capturing image -> {filename}")
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

        image.save(filename)

        print(f"✓ Image saved -> {filename}")

    def stop(self):
        """
        Stop the mock camera.
        """
        print("Camera stopped")

    def is_ready(self):
        """
        Check if the mock camera is ready for capturing images.

        Returns:
            bool: Always returns True for the mock camera.
        """
        return self.ready