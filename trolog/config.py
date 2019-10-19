__all__ = ['Config', 'ConfigException']

import os
from pathlib import Path
import shutil


class ConfigException(Exception):
    pass


class Config(object):
    def __init__(self, basedir='.trolog'):
        self.trolog_path = Path.home() / basedir
        self.config_path = self.trolog_path / 'config'
        self.params = {}
        self.store_name = ''
        self.active_path = None
        self.finished_path = None
        self.ensure_config()
        self.load_config()

    def delete(self):
        shutil.rmtree(str(self.trolog_path))

    def ensure_config(self):
        if not self.trolog_path.exists():
            self.trolog_path.mkdir()

        if not self.config_path.exists():
            with open(str(self.config_path), 'w') as cfgfile:
                cfgfile.write('store_name:default\n')

    def load_config(self):
        with open(str(self.config_path), 'r') as cfgfile:
            for name_value in cfgfile:
                name, value = name_value.rstrip().split(':')
                self.params[name] = value

        self.set_store(self.params['store_name'])

    def update_config(self):
        self.params['store_name'] = self.store_name
        with open(str(self.config_path), 'w') as cfgfile:
            for name in self.params:
                value = self.params[name]
                cfgfile.write('{}:{}\n'.format(name, value))

    def ensure_paths(self):
        if not self.active_path.exists():
            self.active_path.mkdir(parents=True)

        if not self.finished_path.exists():
            self.finished_path.mkdir(parents=True)

    def set_store(self, store_name):
        self.store_name = store_name
        self.store_path = self.trolog_path / 'stores' / store_name
        self.active_path = self.store_path / 'active-timers'
        self.finished_path = self.store_path / 'finished-timers'
        self.ensure_paths()
        self.update_config()

    def wipe_store(self, store_name='default'):
        target_store_path = self.trolog_path / 'stores' / store_name
        if target_store_path.exists():
            shutil.rmtree(str(target_store_path))
        else:
            raise ConfigException('{} does not exist.'.format(store_name))

        if self.store_name == store_name:
            self.set_store('default')

    def has_store(self, store_name):
        store_path = self.trolog_path / 'stores' / store_name
        return store_path.exists()
