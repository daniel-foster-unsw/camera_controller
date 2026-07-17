"""
image_transfer_service.py
"""

from pathlib import Path


class ImageTransferService:

    def load_image(self, filename: Path) -> bytes:
        """
        Load an image from disk.
        """

        with open(filename, "rb") as file:

            return file.read()