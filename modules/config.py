# Interprets config files

import yaml


class ConfigLoader():
    """
    Reads config files.
    """

    def __init__(self, configfile):
        with open(configfile, "r") as f:
            self.loadedconf = yaml.safe_load(f)

    def __getitem__(self, item):
        try:
            return self.loadedconf[item]
        except KeyError:
            print("Argument", item, "not found.")

    def __repr__(self):
        return(self.loadedconf.__repr__())


class UserConfig(ConfigLoader):
    def __init__(self, configfile):
        super().__init__(configfile)


class GlobalConfig(ConfigLoader):
    def __init__(self, configfile):
        super().__init__(configfile)


conf = ConfigLoader("./example_userfiles/config/aliases.yml")
