# Module for pre-parsing user files in preparation for the parser

import os
import regex
from io import StringIO

from bootstraparse.modules import pathresolver as pr
from bootstraparse.modules import environment
import rich

# list of regexps
_rgx_import_file = regex.compile(r'::( ?\< ?(?P<file_name>[\w\-\.\_]+) ?\>[ \s]*)+')
_rgx_import_file_g = "file_name"


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
        self.saved_import_list = None

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
            self.open()
        return self.file.readlines()

    def make_import_list(self):
        """
        Creates a list of all files to be imported.
        Makes sure that the files are not already imported through a previous import statement.
        Recursively build a list of PreParser object for each file to be imported.
        """
        import_list = self.parse_import_list()
        for e, _ in import_list:
            if e in self.list_of_paths:
                raise RecursionError("Error: {} was imported earlier in {}".format(e, self.list_of_paths))
            if e in self.global_dict_of_imports:
                pp = self.global_dict_of_imports[e]
            else:
                pp = PreParser(e, self.__env, self.list_of_paths.copy(), self.global_dict_of_imports)
                self.global_dict_of_imports[e] = pp
                pp.make_import_list()
            self.local_dict_of_imports[e] = pp
        return

    def parse_import_list(self):
        """
        Parses the import list of the file.
        """
        if self.saved_import_list:
            return self.saved_import_list
        import_list = []
        line_count = 0

        for line in self.readlines():
            results = regex.match(_rgx_import_file, line)
            if results:
                for e in results.captures(_rgx_import_file_g):
                    import_list += [(e, line_count)]
            line_count += 1
        # converts relative paths to absolute and returns a table
        self.saved_import_list = [(self.relative_path_resolver(p), l) for p, l in import_list]
        return self.saved_import_list

    def export_with_imports(self):
        """
        Return the file object with all imports done
        """
        temp_file = StringIO()
        source_line_count = 0
        import_list = self.parse_import_list()
        rich.inspect(import_list)
        for p, l in import_list:
            print(os.path.exists(p))

        # todo: test import in sub-folders
        # todo: test same imports on multiple lines

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


if __name__ == "__main__":
    site_path = "../../../example_userfiles/index.bpr"
    __env = environment.Environment()
    michel = PreParser(site_path, __env)
    michel.parse_import_list()
    michel.export_with_imports()