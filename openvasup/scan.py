""" Scan related models from tasks to results """
from model import OpenvasObject
from config import Config, Alert, Scanner, Schedule, Preference
import field as field
from asset import Target

class Filter(object):
    def __init__(self, data={}): pass
    def from_str(self, str): pass


class Task(OpenvasObject):
    """ The Task is a task to scan, which is run against a specific Target """
    name = field.Text().required()
    comment = field.Text()
    alterable = field.Text(editable=False)
    target = field.Object(Target, editable=False).required()
    config = field.Object(Config, editable=False)
    alert = field.Object(Alert)
    observers = field.Object()
    scanner = field.Object(Scanner, editable=False)
    schedule = field.Object(Schedule)
    preference = field.Object(Preference)

    @classmethod
    def get_by_name(cls, name):
        """ Get tasks by name """
        query = {'@filter':'name="%s"' % name}
        return super(Task, cls).get(query)

    def is_container(self):
        """ Is the task a container task? """
        return (self._data['status'] == 'New') and self.target.name is None

    def move(self):
        """ Change what scanner the task uses """
        return self.command('move_task', {
            '@task_id': self.id,
            '@slave_id': self.get_attr('slave_id'),
        })

    def resume(self):
        """ Resume a stopped/paused task """
        return self.command('resume_task', {'@task_id': self.id})

    def start(self):
        """ Start an un-started task """
        return self.command('start_task', {'@task_id': self.id})

    def stop(self):
        """ Stop a running task """
        return self.command('stop_task', {'@task_id': self.id})

    def wait(self): pass


class Report(OpenvasObject):
    """ Specific to a task, hold the results """
    writable = field.Text()
    task = field.Object(Task)
    report_format = field.Object()
    creation_time = field.Object()

    @classmethod
    def get_host(cls, host):
        """ Get reports for a host """
        # @todo check if host is target or asset
        return cls.get({'@host': host})


class ReportFormat(OpenvasObject):
    """ Report format, such as XLS, PDF, etc """
    entity = 'report_format'
    name = field.Text().required()
    summary = field.Text()

class Result(OpenvasObject):
    """ Scan results """
    readonly = True

    @classmethod
    def get_for_task(cls, task):
        """ Get the results for a specific task """
        return cls.get({'@task_id': task.id})

    def as_text(self):
        """ Basic text version of result """
        return "{name} {port} {threat} {severity}".format(**self._data)
