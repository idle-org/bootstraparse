import os

import bootstraparse.modules.config as config
import pytest
import tempfile


temp_folder = tempfile.TemporaryDirectory()
configs = {
    "app/configs/parser_config.yaml": '{"parser": {"name": "test_parser", "type": "test_parser"}}',
    "app/configs/aliases.yaml": '{"parser": {"name": "test_parser", "type": "test_parser"}}',
    "user/config/aliases.yaml": '{"aliases": {"test_alias": "test_parser"}}',
    "user/config/glossary.yaml": '{"glossary": {"test_glossary": "test_parser"}}',
    "user/config/custom_template.yaml": '{"custom_template": {"test_template": "test_parser"}}',
}
bad_configs = {
    "user/bad_config/bad_config.yaml": '{"custom_template": {"test_template": "test_parser',
}
user_conf = os.path.join(temp_folder.name, "user/config")
app_conf = os.path.join(temp_folder.name, "app/configs")
bad_conf = os.path.join(temp_folder.name, "user/bad_config")


@pytest.fixture(autouse=True)
def make_false_configs():
    for file_name, content in configs.items():
        os.makedirs(os.path.dirname(os.path.join(temp_folder.name, file_name)), exist_ok=True)
        with open(os.path.join(temp_folder.name, file_name), "w") as f:
            f.write(content)
    for file_name, content in bad_configs.items():
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
    with pytest.raises(SystemExit):  # Not FileNotFoundError
        assert usr_c["aliases2"] is not None
    assert usr_c.__repr__()


def test_add_to_config():
    usr_c = config.ConfigLoader(user_conf)
    usr_c.add_folder(app_conf)
    from_empty = config.ConfigLoader()
    from_list = config.ConfigLoader([user_conf, app_conf])
    assert from_list["aliases"] == {"aliases": {"test_alias": "test_parser"},
                                    "parser": {"name": "test_parser", "type": "test_parser"}}
    assert from_list["parser_config"] == {"parser": {"name": "test_parser", "type": "test_parser"}}

    with pytest.raises(SystemExit):  # Not FileNotFoundError
        assert from_empty["aliases"]
    from_empty.add_folder(user_conf)
    assert from_empty["aliases"] == {"aliases": {"test_alias": "test_parser"}}

    from_empty.load_from_file(os.path.join(app_conf, "aliases.yaml"))
    assert from_empty["aliases"] == {"aliases": {"test_alias": "test_parser"},
                                     "parser": {"name": "test_parser", "type": "test_parser"}}

    with pytest.raises(SystemExit):
        from_empty.load_from_file(os.path.join(bad_conf, "bad_config.yaml"))


def test_contains():
    usr_c = config.ConfigLoader(user_conf)
    assert "aliases" in usr_c


def test_bad_type():
    with pytest.raises(SystemExit):
        config.ConfigLoader(1)
