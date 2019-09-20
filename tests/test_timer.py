import pytest
from trolog.timer import Timers, TimerException
from trolog.config import Config

@pytest.fixture(scope="function")
def new_config():
    cfg = Config('.')
    cfg.init()
    yield cfg
    cfg.wipe()


def test_startstop_base(new_config):
    t = Timers(new_config)
    t.start('lbl1') 
    t.stop('lbl1') 
    

def test_fail_dup_start(new_config):
    t = Timers(new_config)
    t.start('lbl1') 
    with pytest.raises(TimerException):
        t.start('lbl1') 


def test_fail_nostart_on_stop(new_config):
    t = Timers(new_config)
    t.start('lbl1') 
    with pytest.raises(TimerException):
        t.stop('lbl2') 
