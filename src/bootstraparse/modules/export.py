# Module for final generation of the translated website
import rich
from bootstraparse.modules import config, pathresolver


all_configs = config.ConfigLoader(pathresolver.b_path("configs/"))
all_templates = config.ConfigLoader(pathresolver.b_path("templates/"))
rich.inspect(all_configs)
rich.inspect(all_templates)
