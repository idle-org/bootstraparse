# Interprets config files

import yaml


class ConfigLoader:
    """
    Reads config files
    :param configfile: The file to read
    """

    def __init__(self, configfile):
        """
        Loads config file
        :param configfile: path to config file
        :return: None
        """
        with open(configfile, "r") as f:
            self.loaded_conf = yaml.safe_load(f)

    def __getitem__(self, item):
        """
        Returns config value
        :param item: config key
        :return: config value
        """
        try:
            return self.loaded_conf[item]
        except KeyError:
            print("Argument", item, "not found.")

    def __repr__(self):
        """
        Returns config as string
        :return: config as string
        """
        return self.loaded_conf.__repr__()


class UserConfig(ConfigLoader):
    """
    Reads user config file.
    :param configfile: path to config file
    :return: None
    """
    def __init__(self, configfile):
        super().__init__(configfile)


class GlobalConfig(ConfigLoader):
    """
    Reads global config file.
    :param configfile: path to config file
    :return: None
    """
    def __init__(self, configfile):
        super().__init__(configfile)


# conf = ConfigLoader("./example_userfiles/config/aliases.yml")
