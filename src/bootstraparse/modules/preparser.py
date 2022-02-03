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
        self.path_resolved = pr.pathresolver(path)

    def open(self):
        pass

    def make_import_list(self):
        import_list = self.parse_import_list()
        for e in import_list:
            pp = PreParser(e, self.__env)
            pp.parse_import_list()
            # todo: add to import log list
            # todo: check for recursion errors

    def parse_import_list(self):
        import_list = []
        # parsing the file
        return [self.path_resolved(p) for p in import_list]  # converts relative paths to absolute and returns a table

    def close(self):
        pass

    def __del__(self):
        self.close()


if __name__ == "__main__":
    site_path = "../../../example_userfiles/index.bpr"
    __env = environment.Environment()
    # rich.inspect(__env)

