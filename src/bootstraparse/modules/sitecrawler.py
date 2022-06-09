# Module for file and directories repartition
import os
from bootstraparse.modules import pathresolver, preparser, error_mngr, environment, export


class SiteCrawler:
    """
    A sitecrawler is a generator that yields a tuple of the form (PreParser, file)
    Its goal is to create a list of preparsers and files to be parsed based on
    the files and directories in the initial path.
    This generator is to be used in a for loop to parse all the files and produce
    the final website.
    """
    def __init__(self, path, destination, _env):
        """
        :param path: The path to the directory to be crawled
        :param destination: The path to the directory where the website will be created
        :param _env: The environment object
        :type path: str
        :type destination: str
        :type _env: environment.Environment
        """
        if not os.path.exists(path):
            error_mngr.log_exception(
                FileNotFoundError(f'The specified path "{path}" could not be found.'),
                level="CRITICAL"
            )

        # saved variables
        self._env = _env
        self.initial_path = path
        self.destination_path = destination

        # initialize variables
        self.force_rewrite = self._env.config["parser_config"]["export"]["force_rewrite"]
        self.directories = []
        self.files = []
        self.preparsers = []
        self.global_dict_of_imports = {}

        # dictionaries
        self.authorised_extensions = [".bpr"]
        self.forbidden_folders = ["configs", "config", "templates", "template"]

        # startup operations
        self.get_all_paths()
        self.create_all_paths()

    def get_all_paths(self):
        """
        This method is used to get all the paths to be crawled.
        Its goal is to get all the paths to be crawled and to store them in
        the self.directories and self.files variables.
        """
        self.files, self.directories = self.list_recursively(self.initial_path, self.initial_path)

    def list_recursively(self, path, root):
        """
        Recursive method to get all the paths to be crawled.
        :param path: The current path to be crawled
        :param root: The root path (initial path)
        :type path: str
        :type root: str
        :return: A tuple of the form (files, directories)
        :rtype: (list[(str, str)], list[(str, str)])
        """
        files = []
        directories = []
        for element in os.listdir(path):
            element_fpath = os.path.join(path, element)
            element_rpath = os.path.relpath(path, root)
            if os.path.isdir(element_fpath):
                if element not in self.forbidden_folders:
                    directories.append((element_rpath, element))
                    f, d = self.list_recursively(element_fpath, root)
                    files += f
                    directories += d
            else:
                if os.path.splitext(element)[1] in self.authorised_extensions and element[0] != "_":
                    files.append((element_rpath, element))
        return files, directories

    def create_all_paths(self):
        """
        This method is used to create all the directories in the destination path.
        """
        if not os.path.exists(self.destination_path):
            os.mkdir(self.destination_path)
        for root, di in self.directories:
            temp_path = os.path.join(self.destination_path, root, di)
            if not os.path.exists(temp_path):
                os.mkdir(temp_path)

    def set_all_preparsers(self):
        """
        This method is used to set all the preparsers and initialize them.
        The preparsers are stored in the self.preparsers variable.
        :return: self.preparsers
        :rtype: list[preparser.PreParser]
        """
        for root, file in self.files:
            preparser_path = os.path.join(self.initial_path, root, file)
            pp = preparser.PreParser(preparser_path, self._env, dict_of_imports=self.global_dict_of_imports)
            pp.do_imports()
            p = self.create_file(os.path.join(self.destination_path, root, os.path.splitext(file)[0] + ".html"))
            self.preparsers.append((pp, p))

        return self.preparsers

    def create_file(self, path):
        """
        This method is used to create a file.
        :raises FileExistsError: If the file already exists and the force_rewrite option is False
        :param path: The path to the file to be created
        :type path: str
        """
        if os.path.exists(path):
            if not self.force_rewrite:
                error_mngr.log_exception(
                    FileExistsError(f'File already exists at path "{path}".')
                )
            else:
                os.remove(path)
        open(path, "a").close()
        return path

    def __iter__(self):
        """
        This method is used to iterate over the preparsers and files.
        :yield: A tuple of the form (PreParser, file)
        :ytype: (preparser.PreParser, str)
        """
        for pre in self.preparsers:
            yield pre


if __name__ == "__main__":  # pragma: no cover
    from bootstraparse.modules import config
    site_path = pathresolver.b_path("../../example_userfiles/test.bpr")
    config_path = pathresolver.b_path("../../example_userfiles/configs/")
    _env = environment.Environment()
    _env.config = config.ConfigLoader(config_path)
    __config = config.ConfigLoader(pathresolver.b_path("configs/"))
    __templates = config.ConfigLoader(pathresolver.b_path("templates/"))
    _env.export_mngr = export.ExportManager(__config, __templates)
    xpath = pathresolver.b_path("../../example_userfiles")
    dpath = pathresolver.b_path("../../example_output")
    sc = SiteCrawler(xpath, dpath, _env)
    sc.set_all_preparsers()
    # for p in sc.preparsers:
    #     rich.print(p, "\n")
