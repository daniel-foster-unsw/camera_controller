"""
image_transfer_service.py

Provides image loading services for transferring captured images
to a remote client.
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass
class ImageTransfer:
    filename: str
    filesize: int
    data: bytes


class ImageTransferService:

    def load_image(self, image_path: Path) -> ImageTransfer:
        """
        Load an image from disk.

        Parameters
        ----------
        image_path : Path
            Full path to the image.

        Returns
        -------
        ImageTransfer
            Image metadata and binary data.
        """

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        with open(image_path, "rb") as image_file:
            data = image_file.read()

        return ImageTransfer(
            filename=image_path.name,
            filesize=len(data),
            data=data
        )