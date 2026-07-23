"""
scan.py

Represents one scanning session.
"""
from datetime import datetime
from core.constants import CAMERA_ID

class Scan:
    """ Stores information about one scan session. """
    def __init__(self):
        """Initialise a new scan session."""
        self.camera_id = CAMERA_ID
        self.start_time = datetime.now()
        self.image_number = 0
        

    @property
    def timestamp(self):
        """Return the scan timestamp used for filenames and directories."""
        return self.start_time.strftime("%Y%m%d_%H%M")
        
    @property
    def folder_name(self):
        """Return the scan folder name."""
        return( f"{self.timestamp}_"
        f"{self.camera_id}"
        )
    
    def next_image_number(self):
        """Increment and return the next image number."""
        self.image_number += 1
        return self.image_number
        
    

    