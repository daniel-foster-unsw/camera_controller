class ScanInfo:

    """
    Information about a scan returned by the protocol.
    """

    def __init__(self, scan):

        self.name = scan.folder_name
        self.image_count = scan.image_count