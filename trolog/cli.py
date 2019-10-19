import os
from pathlib import Path
import shutil
from sys import argv

from .config import Config, ConfigException
from .timer import Timers, TimerException

commands = ['init', 'start', 'stop', 'labels', 'switch', 'wipe']


class CommandException(Exception):
    pass


class CLI(object):
    def __init__(self):
        self.config = Config()
        self.timers = Timers(self.config)

    def run(self):
        if len(argv) == 1:
            self.print_usage()
            exit(1)

        command = argv[1]
        if command not in commands:
            print('Unknown command "{}"'.format(argv[1]))
            print()
            self.print_usage()
            exit(1)

        try:
            command_args = argv[2:]
            eval('self.'+command)(command_args)
        except CommandException as ce:
            print(ce)
            exit(1)
        except TimerException as te:
            print(te)
            exit(1)

    def print_usage(self):
        print('Usage:\n')
        print('trolog <command> <command-args>')
        print('\nwhere <command> is one of:\n')
        for cmd in commands:
            print('\t{}'.format(cmd))
        print()

    def init(self, args=[]):
        if len(args) > 1:
            raise CommandException('Extra arguments: {}'.format(args[1:]))
        elif len(args) == 1:
            store_name = args[0]
        else:
            store_name = 'default'

        if self.config.has_store(store_name):
            yn = input('{} exists. Do you wish to overwrite (y/n)? '
                       .format(store_name))
            if yn == 'y':
                print('Overwriting {}.'.format(store_name))
                self.config.set_store(store_name)
            else:
                raise CommandException('Aborting.')
        else:
            print('Creating {}.'.format(store_name))
            self.config.set_store(store_name)

    def switch(self, args=[]):
        if len(args) > 1:
            raise CommandException('Extra arguments: {}'.format(args[1:]))
        elif len(args) == 1:
            store_name = args[0]
        else:
            store_name = 'default'

        self.config.set_store(store_name)

    def wipe(self, args=[]):
        if len(args) > 1:
            raise CommandException('Extra arguments: {}'.format(args[1:]))
        elif len(args) == 1:
            store_name = args[0]
        else:
            store_name = 'default'

        if self.config.has_store(store_name):
            yn = input('Wiping {}. Are you sure (y/n)? '.format(store_name))
            if yn == 'y':
                self.config.wipe_store(store_name)
            else:
                raise CommandException('Aborting.')
        else:
            raise CommandException('{} not found.'.format(store_name))

    def start(self, args=[]):
        if args == []:
            raise CommandException('No label specified for command "start".')
        elif len(args) > 1:
            raise CommandException('Please only specify one label.')
        else:
            label = args[0]
            self.timers.start(label)

    def stop(self, args=[]):
        if args == []:
            raise CommandException('No label specified for command "stop".')
        elif len(args) > 1:
            raise CommandException('Please only specify one label.')
        else:
            label = args[0]
            self.timers.stop(label)

    def labels(self, args=[]):
        if args != []:
            raise CommandException(
                'No command arguments supported for "labels" command.')

        label_list = self.timers.labels()
        for lbl in label_list:
            print(lbl)
