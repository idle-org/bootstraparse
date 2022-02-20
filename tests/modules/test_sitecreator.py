import bootstraparse.modules.sitecreator as sitecreator


def test_create_site():
    sitecreator.create_website()
    sitecreator.create_environment()
    sitecreator.create_config()
    sitecreator.create_crawler()
    sitecreator.create_user_config()
    sitecreator.create_template()
    sitecreator.env_checker()
    sitecreator.begin_crawling(None)
    sitecreator.begin_pre_parsing(None)
    sitecreator.begin_parsing(None)
    sitecreator.begin_export(None)
