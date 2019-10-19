import pytest
from trolog.config import Config, ConfigException

@pytest.fixture(scope="function")
def new_config():
    cfg = Config('./.trolog_test')
    yield cfg
    cfg.delete()


def test_create_and_wipe(new_config):
    cfg = new_config
    cfg.set_store('new_store')
    assert cfg.has_store('new_store')
    cfg.wipe_store('new_store')
    assert not cfg.has_store('new_store')
    assert cfg.store_name == 'default'


def test_fail_wipe_notexist(new_config):
    cfg = new_config
    assert not cfg.has_store('new_store')
    with pytest.raises(ConfigException):
        cfg.wipe_store('new_store')
