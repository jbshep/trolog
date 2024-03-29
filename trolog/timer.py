__all__ = ['Timers', 'TimerException']

from pathlib import Path
import time


def find_invalid_char(label):
    for ch in label:
        if not ch.isalnum():
            return ch
    return ''


class TimerException(Exception):
    pass


class Timers(object):
    def __init__(self, config):
        self.config = config

    def start(self, label):
        invalid_char = find_invalid_char(label)
        if invalid_char != '':
            raise TimerException('Illegal character "{}" found in label.'
                                 .format(invalid_char))

        label_fp = Path(self.config.active_path, label + '.txt')
        if label_fp.exists():
            raise TimerException(
                'Timer for "{}" already started.'.format(label))

        with open(str(label_fp), 'w') as wf:
            wf.write(str(time.time()) + '\n')

    def stop(self, label):
        invalid_char = find_invalid_char(label)
        if invalid_char != '':
            raise TimerException('Illegal character "{}" found in label.'
                                 .format(invalid_char))

        label_fp = Path(self.config.active_path, label + '.txt')
        if not label_fp.exists():
            raise TimerException(
                'Timer for "{}" was never started.'.format(label))

        with open(str(label_fp), 'r') as rf:
            start_time = float(rf.read().rstrip())
            end_time = time.time()
            delta = end_time - start_time

            finished_fp = Path(self.config.finished_path, label + '.txt')
            with open(str(finished_fp), 'a') as wf:
                wf.write('{}:{}:{}\n'.format(start_time, end_time, delta))

        label_fp.unlink()

    def labels(self):
        unsorted_labels = \
            [filepath.stem for filepath in self.config.finished_path.iterdir()]
        return sorted(unsorted_labels)
