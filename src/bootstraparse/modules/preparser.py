# Module for pre-parsing user files in preparation for the parser

import os
from bootstraparse.modules import pathresolver as pr
# from bootstraparse.modules import environment
# import rich


class PreParser:
    """
    Takes a path and environment, executes all pre-parsing methods on the specified file.
    """
    def __init__(self, path, __env, list_of_paths=None, dict_of_imports=None):
        """
        Initializes the PreParser object.
        Takes the following parameters:
            path: the path of the file to be parsed
            __env: the environment object
            path_resolver: the path resolver object, if none is specified, a new one is created with the base path
            list_of_paths: the list of files that have been imported in this branch of the import tree
            dict_of_imports: Dictionary of all imports made to avoid duplicate file opening / pre-parsing
        """
        if list_of_paths is None:
            list_of_paths = []
        if dict_of_imports is None:
            dict_of_imports = {}

        self.__env = __env
        self.path = path
        self.name = os.path.basename(path)
        self.base_path = os.path.dirname(path)
        self.relative_path_resolver = pr.PathResolver(path)
        self.list_of_paths = list_of_paths + [self.relative_path_resolver]
        self.global_dict_of_imports = dict_of_imports
        self.local_dict_of_imports = {}  # Dictionary of all local imports made to avoid duplicate file opening ?
        self.file = None

    def open(self):
        """
        Opens the file and returns a file object.
        """
        self.file = open(self.relative_path_resolver(self.name), 'r')
        return self.file

    def readlines(self):
        """
        Reads the file and returns a list of lines.
        """
        if self.file is None:
            return self.open().readlines()
        return self.file.readlines()

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
                # todo: get the path of the file and append it to the path given
                pp = PreParser(e, self.__env, self.list_of_paths.copy(), self.global_dict_of_imports)
                self.global_dict_of_imports[e] = pp
                pp.parse_import_list()
            self.local_dict_of_imports[e] = pp
        return

    def parse_import_list(self):
        """
        Parses the import list of the file.
        """
        import_list = []
        # todo: parsing the file
        return [self.relative_path_resolver(p) for p in import_list]  # converts relative paths to absolute and returns a table

    def export_with_imports(self):
        """
        Return the file object as a series of lines and append all imports to the file.
        """
        # todo: export the file with all imports
        lines = self.readlines()
        return lines

    def close(self):
        """
        Closes the file.
        """
        if self.file:
            self.file.close()
            self.file = None

    def __del__(self):
        """
        Destructor.
        """
        self.close()

    def __repr__(self):
        """
        Returns a string representation of the PreParser object.
        """
        return "PreParser(path={}, file={}, list_of_paths={}, dict_of_imports={})".format(
            self.path, self.file, self.list_of_paths, self.global_dict_of_imports)

    def __str__(self):
        """
        Returns a string representation of the PreParser object.
        """
        return self.__repr__()


# if __name__ == "__main__":
#     site_path = "../../../example_userfiles/index.bpr"
#     __env = environment.Environment()
#     michel = PreParser(site_path, __env)
#     rich.inspect(michel)
