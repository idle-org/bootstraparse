# Module sequencing the successive actions necessary for website building

def bigmogol():
    """
    First function called by bparse.py, calls all other modules in the right order.
    """
    pass

def create_environment():
    """
    Returns parserEnvironment as an object containing everything needed for app execution.
    """
    pass

def create_config():
    """
    Returns globalConfig as an object from parser_config.yml settings.
    """
    pass

def create_crawler():
    """
    Returns crawler as an object for navigation in the userfiles.
    """
    pass

def create_user_config():
    """
    Returns userConfig as an object from aliases.yml, glossary.yml and website.yml.
    """
    pass

def create_template():
    """
    Returns a templateManager from templates for generating the correct html files.
    """
    pass

def env_checker():
    """
    Verify all is in order for initialisation of the parserEnvironment object and initialises.
    """
    pass

def begin_crawling(pEnv):
    """
    Starts reading every file in the userfiles and adds them to the crawler object progressively.
    """
    pass

def begin_preparsing(pEnv):
    """
    Create an importTree and checks for conflicts or loops; then replaces imports with their contents,
    then replaces all aliases with their values.
    """
    pass

def begin_parsing(pEnv):
    """
    For each of the generated files, parses element after element and creates the graph representation of the website,
    interacts with context_mngr.py to acertain integrity and deal with errors.
    """
    pass

def begin_export():
    """
    Replaces all parsed values with their attributed correspondances as per the template_manager and exports the result as a website.
    """
    pass