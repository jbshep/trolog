import os
from pathlib import Path
import shutil
from sys import argv

'''
trolog init
trolog init remote <ip-address>
trolog start <label>
trolog stop <label>
trolog undo <label>
trolog current
trolog labels
trolog summary
trolog summary <label>
trolog wipe

~/.trolog
    config
    (d) active-timers
    (d) finished-timers
'''

from .config import Config
from .timer import Timers, TimerException

commands = ['init', 'start', 'stop', 'undo', 'current', 'labels',
            'summary', 'wipe']

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
        '''Initializes the ~/.trolog directory and its contents.
        If the directory already exists, users are asked if they wish to overwrite.
        '''
        if args != []:
            raise CommandException(
                'No command arguments supported for "init" command at this time.')
        else:
            if self.config.exists():
                yn = input('{} exists. Do you wish to overwrite (y/n)? '
                        .format(self.config.path))
                if yn == 'y':
                    print('Overwriting {}.'.format(self.config.path))
                    self.config.init()
                else:
                    raise CommandException('Aborting.')
            else:
                print('Creating {}.'.format(self.config.path))
                self.config.init()
    

    def wipe(self, args=[]):
        '''Wipes the ~/.trolog directory. Users are always asked if they are sure.
        '''
        if args != []:
            raise CommandException(
                'No command arguments supported for "wipe" command.')
    
        if self.config.exists():
            yn = input('Wiping. Are you sure (y/n)? '.format(self.config.path))
            if yn == 'y':
                self.config.wipe()
        else:
            raise CommandException(
                ('{} not found. Your environment appears to have been '
                + 'already wiped.').format(self.config.path))
    

    def start(self, args=[]):
        '''Starts timing for a label.
        PRE:
            args has a single label.
            App may or may not have a config dir.
        POST:
            A new active timer has been created.
        EXCEPTIONS:
            Or, a CommandException if command was ill-specified
            or the timer is already running.
        '''
        if args == []:
            raise CommandException('No label specified for command "start".')
        elif len(args) > 1:
            raise CommandException('Please only specify one label.')
        else:
            if not self.config.exists():
                print('First use detected.')
                init()
            label = args[0]
            self.timers.start(label)


    def stop(self, args=[]):
        '''Stops the timing of a label.
        PRE:
            args has a single label.
        POST:
            Active timer has been stopped.
        EXCEPTIONS:
            App may not have a config dir.
            The label's timer may not have been started.
        '''
        if args == []:
            raise CommandException('No label specified for command "stop".')
        elif len(args) > 1:
            raise CommandException('Please only specify one label.')
    
        label = args[0]
    
        if not self.config.exists():
            raise CommandException(
                'Timer for "{}" has not been started.'.format(label))
        else:
            self.timers.stop(label)
    
    
    def labels(self, args=[]):
        if args != []:
            raise CommandException(
                'No command arguments supported for "labels" command.')
    
        label_list = self.timers.labels()
        for lbl in label_list:
            print(lbl)



'''
except Exception as e:
    print('General error: {}'.format(e))
    exit(1)
'''
