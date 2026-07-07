"""
scan_controller.py

Coordinates image acquisition for a scan.
"""

from fileinput import filename
from unittest import result

from core.scan import Scan


class ScanController:

    def __init__(self, storage, camera, logger):

        self.storage = storage
        self.camera = camera
        self.logger = logger

        self.active_scan = None

    def initialise(self, configuration, logger):
        self.active_scan = None
        self.logger = logger
        self.configuration = configuration

    def start_scan(self):

        self.active_scan = Scan()

        #print("✓ Scan Started")
        self.logger.info("Scan initialised.")

#    def start_scan(self):
#        self.active_scan = Scan()
#        print("✓ Scan Started")

    def capture_image(self):

        if self.active_scan is None:
            raise RuntimeError("No active scan.")

        filename = self.storage.get_image_path()

        result = self.camera.capture(filename)
        if result.success:
            #print(f"Captured {filename.name}")
            self.logger.info(f"Captured image: {filename.name}")

        return filename
    
    def stop_scan(self):

        self.active_scan = None

    #    print("✓ Scan Finished")
        self.logger.info(f"Scan finished. Images saved to: {self.storage.scan_directory}")