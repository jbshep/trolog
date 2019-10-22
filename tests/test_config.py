import pytest
from trolog.config import Config, ConfigException


@pytest.fixture(scope="function")
def new_config():
    cfg = Config('./.trolog_test')
    yield cfg
    cfg.delete()


def test_create_and_wipe(new_config):
    cfg = new_config
    cfg.set_project('new_project')
    assert cfg.has_project('new_project')
    cfg.wipe_project('new_project')
    assert not cfg.has_project('new_project')
    assert cfg.project_name == 'default'


def test_fail_wipe_notexist(new_config):
    cfg = new_config
    assert not cfg.has_project('new_project')
    with pytest.raises(ConfigException):
        cfg.wipe_project('new_project')
