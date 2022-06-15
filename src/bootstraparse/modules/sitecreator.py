"""
Module sequencing the successive actions necessary for website building
Usage:
    create_website(origin, destination)
"""

import os

from bootstraparse.modules import pathresolver, sitecrawler, environment, config, export, parser, context_mngr


def create_website(origin, destination):
    """
    First function called by bparse.py,
    calls all other modules in the right order.
    :param origin: The path of the website to be built.
    :param destination: The destination path of the built website.
    :type origin: str
    :type destination: str
    :return: 0 if everything went well, 1 otherwise.
    """
    env = create_environment(origin, destination)
    crwlr = create_crawler(origin, destination, env)
    crwlr.set_all_preparsers()
    crwlr.copy_unparsable_files()
    for element, destination in crwlr:
        save(preparse_parse(element), destination, env)

    return 0


def create_environment(origin, destination):
    """
    Returns parserEnvironment as an object containing
    everything needed for app execution.
    :param origin: The path of the website to be built.
    :param destination: The destination path of the built website.
    :type origin: str
    :type destination: str
    :return: Environment object.
    :rtype: environment.Environment
    """
    env = environment.Environment()
    env.config = config.ConfigLoader(pathresolver.b_path("configs"))
    if os.path.exists(os.path.join(origin, "configs")):
        env.config.add_folder(os.path.join(origin, "configs"))

    env.template = config.ConfigLoader(pathresolver.b_path("templates"))
    if os.path.exists(os.path.join(origin, "templates")):
        env.template.add_folder(os.path.join(origin, "templates"))

    env.export_mngr = export.ExportManager(env.config, env.template)
    env.origin = origin
    env.destination = destination

    return env


def create_crawler(origin, destination, _env):
    """
    Returns crawler as an object for navigation in the user files.
    :param origin: The path of the website to be built.
    :param destination: The destination path of the built website.
    :param _env: The environment object.
    :type origin: str
    :type destination: str
    :type _env: environment.Environment
    :return: Crawler object.
    :rtype: sitecrawler.SiteCrawler
    """
    return sitecrawler.SiteCrawler(origin, destination, _env)


def preparse_parse(preparser):
    """
    Returns a list of containers from a preparser.
    :param preparser: The preparser object.
    :type preparser: parser.Preparser
    :return: List of containers.
    :rtype: list
    """
    io = preparser.do_replacements()
    parsed_list = parser.parse_line(io)
    output = context_mngr.ContextManager(parsed_list, name=preparser.name)()
    return output


def save(list_of_containers, destination, env):
    """
    Saves the list of containers in the destination path.
    :param list_of_containers: The list of containers to be saved.
    :param destination: The destination path.
    :param env: The environment object.
    :type list_of_containers: list
    :type destination: str
    :type env: environment.Environment
    """
    with open(destination, "w") as output_file:
        output_file.write(export.ContextConverter(list_of_containers, env.export_mngr, destination).process_pile().read())


if __name__ == "__main__":  # pragma: no cover
    xpath = pathresolver.b_path("../../example_userfiles")
    dpath = pathresolver.b_path("../../example_output")
    create_website(xpath, dpath)
