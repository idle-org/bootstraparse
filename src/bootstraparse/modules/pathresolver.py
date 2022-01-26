# Module for resolving relative path problems

import os


class pathresolver():
    """
    Intialised with a relative path and returns the translated absolute path
    """

    def __init__(self, basepath):
        self.basepath = os.path.normpath(basepath)

    def __call__(self, relativepath='.'):
        return self.giveabsolute(relativepath)

    def giveabsolute(self, relativepath='.'):
        return os.path.normpath(os.path.join(self.basepath, relativepath))


class boostrapath(pathresolver):
    """
    Initialises pathresolver with the path of the bootstraparse installation folder
    """
    def __init__(self):
        calculatedpath = os.path.join(__file__, "../../")
        super().__init__(calculatedpath)


bpath = boostrapath()
