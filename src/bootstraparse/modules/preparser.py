# Module for pre-parsing user files in preparation for the parser
import logging
import os
import regex
from io import StringIO

from bootstraparse.modules import pathresolver as pr
from bootstraparse.modules import environment
import rich

# list of regexps
_rgx_import_file = regex.compile(r'::( ?\< ?(?P<file_name>[\w\-._/]+) ?\>[ \s]*)+')
_rgx_import_file_g = "file_name"


class PreParser:
    """
    Takes a path and environment, executes all pre-parsing methods on the specified file.
    """
    def __init__(self, path, __env, list_of_paths=None, dict_of_imports=None):
        """
        Initializes the PreParser object.
        Takes the following parameters:
        :param path: the path of the file to be parsed
        :param __env: the environment object
        :param list_of_paths: the list of files that have been imported in this branch of the import tree
        :param dict_of_imports: Dictionary of all imports made to avoid duplicate file opening / pre-parsing
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
        self.list_of_paths = list_of_paths + [self.relative_path_resolver(self.name)]
        self.global_dict_of_imports = dict_of_imports
        self.local_dict_of_imports = {}  # Dictionary of all local imports made to avoid duplicate file opening ?
        self.is_global_dict_of_imports_initialized = False
        self.saved_import_list = None

    def readlines(self):
        """
        Reads the file and returns a list of lines.
        :return: a list of lines
        """
        with open(self.relative_path_resolver(self.name), 'r') as f:
            return f.readlines()

    def make_import_list(self):
        """
        Creates a list of all files to be imported.
        Makes sure that the files are not already imported through a previous import statement.
        Recursively build a list of PreParser object for each file to be imported.
        :return: the dictionary of all files to be imported (key: file name, value: PreParser object)
        """
        import_list = self.parse_import_list()
        if self.is_global_dict_of_imports_initialized:
            return self.local_dict_of_imports

        for e, l in import_list:
            if e in self.list_of_paths:
                raise RecursionError("Error: {} was imported earlier in {}".format(e, self.list_of_paths))
            if e in self.global_dict_of_imports:
                pp = self.global_dict_of_imports[e]
            else:
                try:
                    pp = PreParser(e, self.__env, self.list_of_paths.copy(), self.global_dict_of_imports)
                    self.global_dict_of_imports[e] = pp
                    pp.make_import_list()
                except FileNotFoundError:
                    logging.error("The import {} in file {} line {} doesn't exist".format(e, self.name, l))
                    # TODO: raise a custom exception or define a default behaviour
                    raise ImportError("The import {} in file {} line {} doesn't exist".format(e, self.name, l))
            self.local_dict_of_imports[e] = pp
        self.is_global_dict_of_imports_initialized = True
        return self.local_dict_of_imports

    def parse_import_list(self):
        """
        Parses the import list of the file.
        :return: a list of files to be imported
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
        :return: a filelike object with all imports done
        """

        self.make_import_list()

        temp_file = StringIO()
        source_line_count = 0
        old_import_line = 0
        import_list = self.parse_import_list()
        source_lines = self.readlines()
        for import_path, import_line in import_list:
            if import_line != old_import_line:
                source_line_count += 1
            temp_file.writelines(source_lines[source_line_count:import_line])
            source_line_count = import_line
            import_file = self.global_dict_of_imports[import_path].export_with_imports()
            temp_file.writelines(import_file.readlines())
            old_import_line = import_line
        temp_file.writelines(source_lines[source_line_count:])
        temp_file.seek(0)
        return temp_file

        # todo: test import in sub-folders
        # todo: test same imports on multiple lines

    def __repr__(self):
        """
        Returns a string representation of the PreParser object.
        :return: a string representation of the PreParser object
        """
        return "PreParser(path={}, name={}, base_path={}, " \
               "relative_path_resolver={}, ist_of_paths={}, " \
               "global_dict_of_imports={}, local_dict_of_imports={}" \
               ")".format(self.path, self.name, self.base_path,
                          self.relative_path_resolver, self.list_of_paths,
                          self.global_dict_of_imports, self.local_dict_of_imports)

    def __str__(self):
        """
        Returns a string representation of the PreParser object.
        :return: a string representation of the PreParser object
        """
        return self.__repr__()

    def __eq__(self, other):
        """
        Checks if the PreParser object is equal to another PreParser object.
        :param other: the other PreParser object
        :return: True if the PreParser objects are equal, False otherwise
        """
        if self.path == other.path:
            if self.name == other.name:
                if self.base_path == other.base_path:
                    for elt in self.parse_import_list():
                        if elt not in other.parse_import_list():
                            return False
                    return True
        return False

    def __ne__(self, other):
        """
        Checks if the PreParser object is not equal to another PreParser object.
        :param other: the other PreParser object
        :return: True if the PreParser objects are not equal, False otherwise
        """
        return not self.__eq__(other)

    def rich_tree(self):
        """
        Returns a rich representation of the PreParser object.
        :return: a rich representation of the PreParser object
        """
        pass


# This part is only used for testing
if __name__ == "__main__":  # pragma: no cover
    site_path = "../../../example_userfiles/index.bpr"
    __env = environment.Environment()
    michel = PreParser(site_path, __env)
    michel.parse_import_list()
    # michel.make_import_list()
    michel.export_with_imports()
    with open('../../../example_userfiles/output/show_me_what_you_got.txt', 'w+') as file:
        file.writelines(michel.export_with_imports().readlines())