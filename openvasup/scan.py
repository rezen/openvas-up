""" Scan related models from tasks to results """
from model import OpenvasObject
from config import Config, Alert, Scanner, Schedule, Preference
import field as field
from asset import Target

class Filter(object):
    def __init__(self, data={}): pass
    def from_str(self, str): pass


class Task(OpenvasObject):
    """ @entity task """
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
        query = {'@filter':'name="%s"' % name}
        return super(Task, cls).get(query)

    def is_container(self):
        return (self._data['status'] == 'New') and self.target.name is None
 
    def move(self):
        return self.command('move_task', {
            '@task_id': self.id,
            '@slave_id': self.get_attr('slave_id'),
        })
 
    def resume(self):
        return self.command('resume_task', {'@task_id': self.id})

    def start(self):
        return self.command('start_task', {'@task_id': self.id})
 
    def stop(self):
        return self.command('stop_task', {'@task_id': self.id})

    
    def wait(self): pass


class Report(OpenvasObject):
    """ Specific to a task """
    writable = field.Text()
    task = field.Object(Task)
    report_format = field.Object()
    creation_time = field.Object()

    @classmethod
    def get_host(cls, host):
        # @todo check if host is target or asset
        return cls.get({'@host': host})


class ReportFormat(OpenvasObject):
    entity = 'report_format'
    name = field.Text().required()
    summary = field.Text()

class Result(OpenvasObject):
    """ Scan results """
    readonly = True

    @classmethod
    def get_for_task(cls, task):
        return cls.get({'@task_id': task.id})

    def as_text(self):
        return "{name} {port} {threat} {severity}".format(**self._data)
