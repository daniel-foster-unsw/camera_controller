
"""
configuration.py

Loads and provides access to the Camera Controller configuration.
"""
import json
from pathlib import Path

from core.constants import CONFIG_FOLDER, CONFIG_FILE

class Configuration:
    """
    Manages the configuration settings for the Camera Controller application.
    """
    def __init__(self):
        self.loaded = False
        self.settings = {}
        self.project_root = Path(__file__).resolve().parents[2]
#        self.config_file = (Path(__file__).parent.parent / "config"/"camera.json")

        self.config_file = (
        self.project_root
        / CONFIG_FOLDER
        / CONFIG_FILE
)

    def load(self):
        """
        Loads configuration settings from a file or environment variables.
        """
        try:
            with open(self.config_file, 'r', encoding="utf-8") as file:
                self.settings = json.load(file)
            print("✓  Configuration loaded.")
            self.loaded = True

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_file}"
                )
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Error parsing configuration file: {e}"
                )

        
        return self.settings
    

    def reload(self):
        self.load()
        

    def get(self, *keys):
        """
        Retrieves a configuration value using a sequence of keys.
        """
        value = self.settings

        for key in keys:
            if not isinstance(value, dict):
                raise KeyError(
                    f"'{key}' cannot be accessed because the current value is not a dictionary."
                )

            value = value.get(key)

            if value is None:
                raise KeyError(
                    f"Configuration key '{key}' not found."
                )

        return value
    
    

    def __str__(self):
        return f"Configuration({self.config_file})"