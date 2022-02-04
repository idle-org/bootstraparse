# Module for pre-parsing user files in preparation for the parser

import os
from bootstraparse.modules import environment
from bootstraparse.modules import pathresolver as pr
import rich


class PreParser:
    """
    Takes a path and environment, executes all pre-parsing methods on the specified file.
    """
    def __init__(self, path, __env):
        self.path = path
        self.__env = __env
        self.path_resolved = pr.PathResolver(path)

    def open(self):
        pass

    def make_import_list(self):
        """
        Creates a list of all files to be imported.
        Makes sure that the files are not already imported through a previous import statement.
        Recursively build a list of PreParser object for each file to be imported.
        """
        import_list = self.parse_import_list()
        for e in import_list:
            pp = PreParser(e, self.__env)
            pp.parse_import_list()
            # todo: add to import log list
            # todo: check for recursion errors

    def parse_import_list(self):
        """
        Parses the import list of the file.
        """
        import_list = []
        # parsing the file
        return [self.path_resolved(p) for p in import_list]  # converts relative paths to absolute and returns a table

    def close(self):
        """
        Closes the file.
        """
        pass

    def __del__(self):
        """
        Destructor.
        """
        self.close()


if __name__ == "__main__":
    site_path = "../../../example_userfiles/index.bpr"
    __env = environment.Environment()
    # rich.inspect(__env)
