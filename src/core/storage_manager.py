"""
storage_manager.py

Handles image storage and file management.
"""

from pathlib import Path
from datetime import datetime
from core.constants import (IMAGE_FOLDER, CAMERA_ID, IMAGE_EXTENSION)
import shutil
from core.scan import Scan







class StorageManager:
    def __init__(self, scan):
        self.scan = scan

        self.logger = None
        self.project_root = Path(__file__).resolve().parents[1]
        storage_directory = None
        self.image_directory = None
#        self.image_directory =( self.project_root / IMAGE_FOLDER)
        # Image number within this scan
        #self.image_number = 0

        # Timestamp created once when scan starts
        #self.scan_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        # Scan folder name
        

        #self.scan.folder_name = (f"{self.scan.timestamp}_{CAMERA_ID}")
        # Fuull path to this scan
        #self.scan_directory = (self.image_directory / self.scan_folder_name)
        self.scan_directory = None

    def initialise(self,configuration, logger):
        try:
            self.logger = logger
            storage_directory = configuration.get("storage", "directory")
            self.image_directory = (self.project_root / storage_directory).resolve()
            self.scan_directory = (self.image_directory / self.scan.folder_name)

            self.image_directory.mkdir(parents=True, exist_ok=True)
            self.scan_directory.mkdir(parents=True, exist_ok=True)

            print("✓ Storage ready.")

        except Exception as ex:
            print("Failed to initalise storage")
            raise

    def check_storage(self):
        try:
            usage = shutil.disk_usage(self.project_root)
            

            return {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free
            }
        except Exception as ex:
            self.logger.error(f"Failed to check storage: {ex}")
            raise



    def image_count(self):
        return len(list(self.image_directory.glob("*")))
    
    def get_next_filename(self):
        try:
            #self.image_number += 1
            image_number = self.scan.next_image_number()
            filename = (
                f"{self.scan.timestamp}_"
                f"{CAMERA_ID}_"
                f"{image_number:06d}"
                f"{IMAGE_EXTENSION}"
            )
            return filename
        
        except Exception as ex:
            self.logger.error(f"Failed to generate filename: {ex}")
            raise
    
    def get_image_path(self):
        return(self.scan_directory / self.get_next_filename())
    
    

    def find_image_path(self, filename: str):
        self.logger.info(f"Searching for image: {filename}")


        for path in self.image_directory.rglob(filename):
            self.logger.info(f"Found image: {path}")
            return path
        

        self.logger.warning(f"Image not found: {filename}")
        raise FileNotFoundError(f"Image not found: {filename}")



    def delete_image(self, filename: str) -> bool:

        """
        Delete an image.

        Returns
        -------
        True: Image deleted.
        False: Image not found.
        """
        try:
            image_path = self.find_image_path(filename)


            if image_path is None:
                self.logger.warning(f"Image not found: {filename}")
                return False

            """
            if not image_path.exists():

                self.logger.warning(
                    f"Image not found: {filename}"
                )
            
                return False
            """


            
            image_path.unlink()

            self.logger.info(f"Deleted image: {filename}")

            return True
    
        except FileNotFoundError:
            self.logger.warning(f"Image not found: {filename}")
            return False

        except Exception as ex:
            self.logger.error(f"Failed to delete image '{filename}': {ex}")
            return False
        

    def list_images(self):
        """
        Return all scans and their images.

        Returns
        -------
        list
            [
                {
                    "scan": "...",
                    "images": [
                        {
                            "filename": "...",
                            "filesize": 12345
                        }
                    ]
                }
            ]
        """

        scans = []

        self.logger.info("Listing stored images...")

        for scan_directory in sorted(self.image_directory.iterdir()):

            if not scan_directory.is_dir():
                continue

            scan = {
                "scan": scan_directory.name,
                "images": []
            }

            for image in sorted(scan_directory.glob(f"*{IMAGE_EXTENSION}")):

                scan["images"].append(
                    {
                        "filename": image.name,
                        "filesize": image.stat().st_size
                    }
                )

            scans.append(scan)

        self.logger.info(f"Found {len(scans)} scan(s).")

        return scans





    
 