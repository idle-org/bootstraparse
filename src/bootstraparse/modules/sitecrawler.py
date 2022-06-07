# Module for file and directories repartition
import os
from bootstraparse.modules import pathresolver, preparser, error_mngr, environment, export


class SiteCrawler:
    def __init__(self, path, destination, _env):
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
        self.force_rewrite = True  # TODO: read from config
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
        for root, directory, files in os.walk(self.initial_path):
            for name in files:
                if os.path.splitext(name)[1] in self.authorised_extensions and name[0] != "_":
                    self.files.append((os.path.relpath(root, self.initial_path), name))

            for name in directory:
                if name not in self.forbidden_folders:
                    self.directories.append((os.path.relpath(root, self.initial_path), name))
                    # TODO: handle recursively

    def create_all_paths(self):
        if not os.path.exists(self.destination_path):
            os.mkdir(self.destination_path)
        for root, di in self.directories:
            temp_path = os.path.join(self.destination_path, root, di)
            if not os.path.exists(temp_path):
                os.mkdir(temp_path)

    def set_all_preparsers(self):
        for root, file in self.files:
            preparser_path = os.path.join(self.initial_path, root, file)
            pp = preparser.PreParser(preparser_path, self._env, dict_of_imports=self.global_dict_of_imports)
            pp.do_imports()
            p = self.create_file(os.path.join(self.destination_path, root, os.path.splitext(file)[0] + ".html"))
            self.preparsers.append((pp, p))

        return self.preparsers

    def create_file(self, path):
        if os.path.exists(path):
            if not self.force_rewrite:
                error_mngr.log_exception(
                    FileExistsError(f'File already exists at path "{path}".')
                )
            else:
                os.remove(path)
        open(path, "w+").close()
        return path

    def __iter__(self):
        for pre in self.preparsers:
            yield pre


if __name__ == "__main__":
    from bootstraparse.modules import config
    site_path = pathresolver.b_path("../../example_userfiles/test.bpr")
    config_path = pathresolver.b_path("../../example_userfiles/configs/")
    _env = environment.Environment()
    _env.config = config.ConfigLoader(config_path)
    __config = config.ConfigLoader(pathresolver.b_path("configs/"))
    __templates = config.ConfigLoader(pathresolver.b_path("templates/"))
    _env.export_mngr = export.ExportManager('', '', __config, __templates)
    xpath = pathresolver.b_path("../../example_userfiles")
    dpath = pathresolver.b_path("../../example_output")
    sc = SiteCrawler(xpath, dpath, _env)
    sc.set_all_preparsers()
    # for p in sc.preparsers:
    #     rich.print(p, "\n")
