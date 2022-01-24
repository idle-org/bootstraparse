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
        return self.loadedconf[item]

class UserConfig(ConfigLoader):
    def __init__(self, configfile):
        super().__init__(configfile)

class GlobalConfig(ConfigLoader):
    def __init__(self, configfile):
        super().__init__(configfile)
        

conf = ConfigLoader("./example_userfiles/config/aliases.yml")
