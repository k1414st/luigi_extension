"""
TODO: logs timestamp to DB.
"""
from pathlib import Path
import luigi


class ExternalWatcher(luigi.Task):
    """
    This task acts like ExternalTask but watches its sources timestamp.
    If sources timestamp is updated, this task runs and updates subsequent tasks.
    
    (Actually, this task output empty file named its task name and timestamp.
     and check consistency of source-timestamp and output task-timestamp.)

    You can use this class by inheritting like ExternalTask,
    but you must implement only 'watches' method, instead of 'requires' method.
    ('watches' target must be only 1 target.)
    """

    timestamp_path = luigi.Parameter()

    def watches(self):
        """ User must implement this method returns string of source file. """
        raise NotImplementedError

    def requires(self):
        watched = self.watches()

        class __External(luigi.ExternalTask):
            def requires(self):
                return watched

            def output(self):
                return luigi.LocalTarget(self.requires())

        return __External()

    def main_output(self):
        return luigi.LocalTarget(self.watches())

    def __timestamp_output(self):
        mtime = self.timestamp_path + '/' + \
            self.__class__.__name__ + '_' + str(Path(self.watches()).stat().st_mtime)
        return luigi.LocalTarget(mtime)

    def output(self):
        return {'main': self.main_output(), 'check_update': self.__timestamp_output()}

    def run(self):
        Path(self.__timestamp_output().path).touch()


class WatcherTask(luigi.Task):
    """
    This abstract class inherits watchers by requiring ExternalWatcher objects.
    User must implement run and 'main_output' method, instead of 'output' method,
    and you can draw input and output tasks by 'main_input' and 'main_oputput' methods.
    """
    def main_output(self):
        raise NotImplementedError

    def main_input(self):
        return self.input()['main']

    def output(self):
        return {'main': self.main_output(),
                'check_update': self.requires().output()['check_update']}

