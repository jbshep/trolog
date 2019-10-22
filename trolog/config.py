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
        self.project_name = ''
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
                cfgfile.write('project_name:default\n')

    def load_config(self):
        with open(str(self.config_path), 'r') as cfgfile:
            for name_value in cfgfile:
                name, value = name_value.rstrip().split(':')
                self.params[name] = value

        self.set_project(self.params['project_name'])

    def update_config(self):
        self.params['project_name'] = self.project_name
        with open(str(self.config_path), 'w') as cfgfile:
            for name in self.params:
                value = self.params[name]
                cfgfile.write('{}:{}\n'.format(name, value))

    def ensure_paths(self):
        if not self.active_path.exists():
            self.active_path.mkdir(parents=True)

        if not self.finished_path.exists():
            self.finished_path.mkdir(parents=True)

    def set_project(self, project_name):
        self.project_name = project_name
        self.project_path = self.trolog_path / 'projects' / project_name
        self.active_path = self.project_path / 'active-timers'
        self.finished_path = self.project_path / 'finished-timers'
        self.ensure_paths()
        self.update_config()

    def wipe_project(self, project_name='default'):
        target_project_path = self.trolog_path / 'projects' / project_name
        if target_project_path.exists():
            shutil.rmtree(str(target_project_path))
        else:
            raise ConfigException('{} does not exist.'.format(project_name))

        if self.project_name == project_name:
            self.set_project('default')

    def has_project(self, project_name):
        project_path = self.trolog_path / 'projects' / project_name
        return project_path.exists()
