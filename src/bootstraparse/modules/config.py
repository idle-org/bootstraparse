# Interprets config files
import os

import yaml


class ConfigLoader:
    """
    Reads all config files in a folder
    Behaves like a dictionary of all config files
    return FileNotFound Error on Error
    :param config_folder: The folder to read
    """

    def __init__(self, config_folder, extensions="yaml"):
        """
        Defines the config folder and loads all configs
        :param config_folder: path to config file
        :param extensions: file extensions to load
        :return: None
        """
        self.config_folder = config_folder
        self.loaded_conf = {}
        self.extensions = extensions
        self.load_configs()

    def load_from_file(self, filepath):
        """
        Loads a config file
        :param filepath: path to config file
        :return: None
        """
        basename = os.path.basename(filepath)
        name, ext = os.path.splitext(basename)
        with open(filepath, "r") as f:
            self.loaded_conf[name] = yaml.safe_load(f)

    def load_configs(self):
        """
        Loads all configs in the config folder
        :return: None
        """
        for filename in os.listdir(self.config_folder):
            file_ext = os.path.splitext(filename)[1][1:]
            if file_ext in self.extensions:
                self.load_from_file(os.path.join(self.config_folder, filename))

    def __getitem__(self, item):
        """
        Returns a yaml config object if in self.loaded_conf
        :param item: config key
        :return: config value
        """
        try:
            return self.loaded_conf[item]
        except KeyError:
            print(f"Error: {item} is not in {self.loaded_conf}")
            raise FileNotFoundError

    def __repr__(self):
        """
        Returns config as string
        :return: config as string
        """
        return self.loaded_conf.__repr__()


class UserConfig(ConfigLoader):
    """
    Reads user config file.
    :param config_folder: path to config file
    :return: None
    """
    def __init__(self, config_folder):
        super().__init__(config_folder)


class GlobalConfig(ConfigLoader):
    """
    Reads global config file.
    :param config_folder: path to config file
    :return: None
    """
    def __init__(self, config_folder):
        super().__init__(config_folder)


# conf = ConfigLoader("./example_userfiles/config/aliases.yaml")
