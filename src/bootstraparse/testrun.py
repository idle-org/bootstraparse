import modules.sitecreator as sitecreator
from rich import print, pretty, inspect


pretty.install()


conf = sitecreator.create_config()
print("[red]test",conf)
inspect(conf)