from dataclasses import dataclass


@dataclass
class ScanInfo:
    
    """
    Information about a scan returned by the protocol.
    """
    scan: str

    
    """
    def __init__(self, scan):

        self.name = scan.folder_name
        #self.image_count = scan.image_count

    """