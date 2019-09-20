import os
from pathlib import Path
import shutil

DEFAULT_LOCAL_CONFIG = '.trolog'

class Config(object):
    def __init__(self, base=os.environ['HOME']):
        self.path = Path(base, DEFAULT_LOCAL_CONFIG)
        self.active_path = Path(self.path, 'active-timers')
        self.finished_path = Path(self.path, 'finished-timers')


    def exists(self):
        return self.path.exists() and self.active_path.exists() \
            and self.finished_path.exists()


    def init(self):
        if self.exists():
            shutil.rmtree(str(self.path))

        self.path.mkdir()
        self.active_path.mkdir()
        self.finished_path.mkdir()


    def wipe(self):
        if self.exists():
            shutil.rmtree(str(self.path))
