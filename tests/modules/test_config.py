import os

import bootstraparse.modules.config as config
import pytest
import tempfile


temp_folder = tempfile.TemporaryDirectory()
configs = {
    "app/configs/parser_config.yaml": '{"parser": {"name": "test_parser", "type": "test_parser"}}',
    "user/config/aliases.yaml": '{"aliases": {"test_alias": "test_parser"}}',
    "user/config/glossary.yaml": '{"glossary": {"test_glossary": "test_parser"}}',
    "user/config/custom_template.yaml": '{"custom_template": {"test_template": "test_parser"}}',
}

user_conf = os.path.join(temp_folder.name, "user/config")
app_conf = os.path.join(temp_folder.name, "app/configs")


@pytest.fixture(autouse=True)
def make_false_configs():
    for file_name, content in configs.items():
        os.makedirs(os.path.dirname(os.path.join(temp_folder.name, file_name)), exist_ok=True)
        with open(os.path.join(temp_folder.name, file_name), "w") as f:
            f.write(content)


def test_config_load():
    usr_c = config.ConfigLoader(user_conf)
    assert usr_c["aliases"] == {"aliases": {"test_alias": "test_parser"}}
    assert usr_c["glossary"] == {"glossary": {"test_glossary": "test_parser"}}
    assert usr_c["aliases"]["aliases"] == {"test_alias": "test_parser"}
    assert usr_c["aliases"]["aliases"]["test_alias"] == "test_parser"
    with pytest.raises(KeyError):
        assert usr_c["aliases"]["aliases"]["test_alias2"] is not None
    with pytest.raises(FileNotFoundError):
        assert usr_c["aliases2"] is not None
    assert usr_c.__repr__()


def test_children():
    usr_c = config.UserConfig(user_conf)
    site_c = config.GlobalConfig(app_conf)
    assert usr_c["glossary"] == {"glossary": {"test_glossary": "test_parser"}}
    assert site_c["parser_config"] == {"parser": {"name": "test_parser", "type": "test_parser"}}
