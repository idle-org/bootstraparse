# Module for resolving relative path problems

import os


class PathResolver:
    """
    Initialised with a relative path and returns the translated absolute path
    """

    def __init__(self, base_path):
        self.base_path = os.path.normpath(os.path.dirname(base_path))

    def __call__(self, relative_path='.'):
        return self.give_absolute(relative_path)

    def give_absolute(self, relative_path='.'):
        return os.path.normpath(os.path.join(self.base_path, relative_path))


class BoostraPath(PathResolver):
    """
    Initialises PathResolver with the path of the bootstraparse installation folder
    """
    def __init__(self):
        calculated_path = os.path.join(__file__, "../../")
        super().__init__(calculated_path)


b_path = BoostraPath()
