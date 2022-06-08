# Interprets config files
# The Config will be loaded by the environment at runtime and should be accessed that way
# Usage:
#  from bootstraparse.modules.config import ConfigLoader
#  config = ConfigLoader([list of config files], extensions=[list of extensions])
#  config['file']['key']
# The ConfigLoader class has load_from_file and load_from_folder methods and __getitem__ for accessing loaded elements

import os

import rich
import yaml
from bootstraparse.modules import error_mngr


class ConfigLoader:
    """
    Reads all config files in a folder
    Behaves like a dictionary of all config files
    """

    def __init__(self, config_folder=None, extensions=("yaml", "yml")):
        """
        Defines the config folder and loads all configs
        :param config_folder: path to config file
        :type config_folder: (str | list[str])
        :param extensions: file extensions to load
        :type extensions: list[str]
        :raise TypeError: if config_folder is not a string or a list of strings
        """
        if config_folder is None:
            self.config_folders = []
        elif isinstance(config_folder, str):
            self.config_folders = [config_folder]
        elif isinstance(config_folder, (list, tuple)):
            self.config_folders = config_folder
        else:
            error_mngr.log_exception(TypeError(f"Incorrect config type given. Expected a string, list or tuple; "
                                               f"got {type(config_folder).__name__} instead."), level='CRITICAL')
        self.loaded_conf = {}
        self.extensions = extensions
        self.reload_all()

    def reload_all(self):
        """
        Reloads all configs
        :return: None
        """
        self.loaded_conf = {}
        for folder in self.config_folders:
            self.load_from_folder(folder)

    def add_folder(self, folder):
        """
        Add a Folder to the list of configs
        :param folder: path to folder
        :type folder: str
        :return: None
        """
        self.config_folders.append(folder)
        self.load_from_folder(folder)

    def load_from_file(self, filepath):
        """
        Loads a config file
        :param filepath: path to config file
        :type filepath: str
        :return: None
        """
        basename = os.path.basename(filepath)
        name, ext = os.path.splitext(basename)
        with open(filepath, "r") as f:
            try:
                if name not in self.loaded_conf:
                    self.loaded_conf[name] = yaml.safe_load(f)
                else:
                    self.loaded_conf[name].update(yaml.safe_load(f))
                    error_mngr.log_message(f"Warning: {name} is already in {self.loaded_conf}", level='INFO')
            except BaseException as e:
                error_mngr.log_message(f'Error parsing in file {basename} at {filepath}.', level='CRITICAL')
                error_mngr.log_exception(str(e), level='CRITICAL')

    def load_from_folder(self, folder):
        """
        Loads all configs in the config folder
        :param folder: path to folder
        :type folder: str
        :return: None
        """
        for filename in os.listdir(folder):
            file_ext = os.path.splitext(filename)[1][1:]
            if file_ext in self.extensions:
                self.load_from_file(os.path.join(folder, filename))

    def __getitem__(self, item):
        """
        Returns a yaml config object if in self.loaded_conf
        :param item: config key
        :type item: str
        :raise KeyError: if item is not in self.loaded_conf
        :return: config value
        """
        try:
            return self.loaded_conf[item]
        except KeyError:  # make sure getitem is never used
            error_mngr.log_exception(KeyError(f"Error: {item} is not in {self.loaded_conf}"), level='CRITICAL')

    def __contains__(self, item):
        """
        Same as a dictionary.
        :param item: config key
        :type item: str
        :return: True if item is in self.loaded_conf
        """
        return item in self.loaded_conf

    def __repr__(self):
        """
        Returns config as string
        :return: the dict of configs and their values
        :rtype: str
        """
        return str(self.loaded_conf.__repr__())


if __name__ == '__main__':  # pragma: no cover
    conf = ConfigLoader("../configs/")
    conf.add_folder("../../../example_userfiles/config/")
    rich.inspect(conf)
