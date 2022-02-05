# Module for pre-parsing user files in preparation for the parser

import os
from bootstraparse.modules import environment
from bootstraparse.modules import pathresolver as pr
import rich


class PreParser:
    """
    Takes a path and environment, executes all pre-parsing methods on the specified file.
    """
    def __init__(self, path, __env, list_of_paths=[], dict_of_imports={}):
        self.path = path
        self.__env = __env
        self.path_resolved = pr.PathResolver(path)
        self.list_of_paths = list_of_paths + [self.path_resolved]  # List of files in a branch of imports until its end
        self.global_dict_of_imports = dict_of_imports  # Dictionary of all imports made to avoid duplicate file opening
        self.local_dict_of_imports = {}

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
            if e in self.list_of_paths:
                raise RecursionError("Error: {} was imported earlier in {}".format(e, self.list_of_paths))
            if e in self.global_dict_of_imports:
                pp = self.global_dict_of_imports[e]
            else:
                pp = PreParser(e, self.__env, self.list_of_paths.copy(), self.global_dict_of_imports)
                self.global_dict_of_imports[e] = pp
                pp.parse_import_list()
        return

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
    michel = PreParser(site_path, __env)
    rich.inspect(michel)
