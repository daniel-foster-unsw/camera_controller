"""
logger_manager.py

Creates and manages the application logger.
"""


import logging
from pathlib import Path


class LoggerManager:

   def __init__(self):
      """Initialise the logger manager."""
      self.configuration = None

      self.logger = None

      self.log_file = None

   def initialise(self, configuration):
      """Log an informational message."""
      self.configuration = configuration
      

      log_directory = (
         Path(__file__).resolve().parents[1]
         / self.configuration.get("logging", "directory")
      )

      log_directory.mkdir(parents=True, exist_ok=True)

      log_file = log_directory / "camera_controller.log"
      self.log_file = log_file


      self.logger = logging.getLogger("CameraController")

      self.logger.setLevel(
         getattr(
            logging,
            self.configuration.get("logging", "level")
         )
      )
      #Create the Formatter
      formatter = logging.Formatter(
         "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
         "%Y-%m-%d %H:%M:%S"
      )
      #creatr the console handler
      console = logging.StreamHandler()

      console.setFormatter(formatter)

      self.logger.addHandler(console)

      #create the file handler
      file_handler = logging.FileHandler(
         log_file,
         encoding="utf-8"
      )

      file_handler.setFormatter(formatter)

      self.logger.addHandler(file_handler)
      
   #Conveinence method to log messages
   def info(self, message):
      """Log an informational message."""
      self.logger.info(message)


   def warning(self, message):
      """Log a warning message."""
      self.logger.warning(message)


   def error(self, message):
      """Log an error message."""
      self.logger.error(message)


   def debug(self, message):
      """Log a debug message."""
      self.logger.debug(message)


   def get_log_file(self):
      """Return the current log file path."""
      return self.log_file