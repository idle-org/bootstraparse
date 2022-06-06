# Module sequencing the successive actions necessary for website building
import os
import rich
from bootstraparse.modules import pathresolver, sitecrawler, environment, config, export, parser, context_mngr


def create_website(origin, destination):
    """
    First function called by bparse.py,
    calls all other modules in the right order.
    """
    env = create_environment(origin, destination)
    crwlr = create_crawler(origin, destination, env)
    crwlr.set_all_preparsers()
    for element, destination in crwlr:
        save(preparse_parse(element), destination, env)


def create_environment(origin, destination):
    """
    Returns parserEnvironment as an object containing
    everything needed for app execution.
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
    """
    return sitecrawler.SiteCrawler(origin, destination, _env)


def preparse_parse(preparser):
    io = preparser.do_replacements()
    parsed_list = parser.parse_line(io)
    output = context_mngr.ContextManager(parsed_list)()
    return output


def save(list_of_containers, destination, env):
    with open(destination, "w") as output_file:
        output_file.write(export.ContextConverter(list_of_containers, env.export_mngr).process_pile().read())


if __name__ == "__main__":
    xpath = pathresolver.b_path("../../example_userfiles")
    dpath = pathresolver.b_path("../../example_output")
    create_website(xpath, dpath)

