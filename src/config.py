from pathlib import Path
import json

class Config:
    def __init__(self, config_file=None):
        self.default_directory = Path.cwd()
        self.default_conda_env = "base"
        self.settings = {
            "directory": str(self.default_directory),
            "conda_env": self.default_conda_env
        }
        if config_file:
            self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            self.settings.update(json.load(f))

    def update_settings(self, directory=None, conda_env=None):
        if directory:
            self.settings["directory"] = str(Path(directory).resolve())
        if conda_env:
            self.settings["conda_env"] = conda_env

    def get_settings(self):
        return self.settings