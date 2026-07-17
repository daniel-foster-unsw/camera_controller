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

    def initialise(self,configuration):

        storage_directory = configuration.get("storage", "directory")
        self.image_directory = (self.project_root / storage_directory).resolve()
        self.scan_directory = (self.image_directory / self.scan.folder_name)

        self.image_directory.mkdir(parents=True, exist_ok=True)
        self.scan_directory.mkdir(parents=True, exist_ok=True)

        print("✓ Storage ready.")

    def check_storage(self):
        usage = shutil.disk_usage(self.project_root)

        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free
        }
    def image_count(self):
        return len(list(self.image_directory.glob("*")))
    
    def get_next_filename(self):
        #self.image_number += 1
        image_number = self.scan.next_image_number()
        filename = (
            f"{self.scan.timestamp}_"
            f"{CAMERA_ID}_"
            f"{image_number:06d}"
            f"{IMAGE_EXTENSION}"
        )
        return filename
    
    def get_image_path(self):
        return(self.scan_directory / self.get_next_filename())
    
    

    def get_image_path(self, filename: str):
        for path in self.image_directory.rglob(filename):
            return path

        raise FileNotFoundError(f"Image not found: {filename}")
    
 