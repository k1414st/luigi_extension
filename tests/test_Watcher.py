from pathlib import Path
import luigi
from luigi.util import requires
from luigi_extension import ExternalWatcher, WatcherTask


class WatchFoo(ExternalWatcher):
    """ watches timestamp of foo.txt """
    def watches(self):
        return './foo.txt'
        
@requires(WatchFoo)
class TaskA(WatcherTask):
    """ checks timestamp of watched files (foo.txt) and update """
    def main_output(self):
        return luigi.LocalTarget('./bar.txt')

    def run(self):
        inputs = self.main_input()
        with inputs.open('r') as f:
            input_str = ''.join(f.readlines())
        with open(self.main_output().path, 'w') as f:
            f.write(f'*** {input_str} ***')

@requires(TaskA)
class TaskB(WatcherTask):
    """ checks timestamp of watched files (foo.txt) and update """
    def main_output(self):
        return luigi.LocalTarget('./baz.txt')

    def run(self):
        inputs = self.main_input()
        with inputs.open('r') as f:
            input_str = ''.join(f.readlines())
        with open(self.main_output().path, 'w') as f:
            f.write(f'<<< {input_str} >>>')
    

def test_watcher():
    """ test ExternalWatcher & WatcherTask """
    luigi.build([TaskB(timestamp_path='tmp')], local_scheduler=True, workers=4)


if __name__ == '__main__':
    test_watcher()

