""" Scan related models from tasks to results """
from datetime import datetime
from model import OpenvasObject
from secinfo import Config
from config import Alert, Scanner, Schedule, Preference
import field as field
from asset import Target
from secinfo import Nvt
import time

class Filter(object):
    def __init__(self, data={}): pass
    def from_str(self, str): pass


class Task(OpenvasObject):
    """ The Task is a task to scan, which is run against a specific Target """
    name = field.Text().required()
    comment = field.Text()
    status = field.Text(editable=False)
    alterable = field.Text(editable=False)
    target = field.Object(Target, editable=False).required()
    config = field.Object(Config, editable=False)
    alert = field.Object(Alert)
    observers = field.Object()
    scanner = field.Object(Scanner, editable=False)
    schedule = field.Object(Schedule)
    preference = field.Object(Preference)

    def is_tagged(self):
        """ Has the task been tagged? """
        if 'user_tags' not in self._data:
            # @todo make sure data has been fetched
            return False
        return int(self.get_attr('user_tags')['count']) > 0

    def get_last_duration(self):
        """ Get the duration of scan based on the last report """
        if 'last_report' not in self._data:
            return None

        report = self._data['last_report']['report']
        end = datetime.strptime(report['scan_end'], '%Y-%m-%dT%H:%M:%SZ')
        start = datetime.strptime(report['scan_start'], '%Y-%m-%dT%H:%M:%SZ')
        return  end - start

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

    def is_active(self):
        return not (self.status == 'Stopped' or self.status == 'Done')

    def wait_to_complete(self, interval=60, max_time=60):
        """ Interval is in seconds and max_time is in minutes """
        while self.is_active():
            time.sleep(interval)
            self.reload()
        return self


class ReportFormat(OpenvasObject):
    """ Report format, such as XLS, PDF, etc """
    entity = 'report_format'
    name = field.Text().required()
    summary = field.Text()


class Report(OpenvasObject):
    """ Specific to a task, hold the results """
    writable = field.Text()
    task = field.Object(Task)
    report_format = field.Object(ReportFormat)
    creation_time = field.Object()

    def get_extension(self):
        """ The file extension for the report """
        return self._data['@extension']

    def is_spreadsheet(self):
        """ Is the report a spreadsheet? """
        return self.get_extension() in ['xls', 'csv']

    def get_host(self):
        """ Get info on the host for the report """
        return self._data['report']['host']

    def get_results(self):
        """ Get all the report results as Result instances """
        return [Result(result) for result in self._data['report']['results']['results']]

    @classmethod
    def get_by_host(cls, host):
        """ Get reports for a host """
        # @todo check if host is target or asset
        return cls.get({'@host': host})


class Result(OpenvasObject):
    """ Scan results """
    readonly = True
    host = field.Text()

    @classmethod
    def get_for_task(cls, task):
        """ Get the results for a specific task """
        return cls.get({'@task_id': task.id})

    def add_note(self): pass

    def add_overide(self): pass

    def get_host(self):
        host = self._data['host']
        if host['asset'] is not None:
            print(host['asset'])
            exit()
        return host['$text']

    def as_text(self):
        """ Basic text version of result """
        data = {
            'name': self._data.get('name'),
            'host' : self.get_host(),
            'port': self._data.get('port'),
            'threat':self._data.get('threat'),
            'severity':self._data.get('severity'),
        }
        
        if data['name'] is None:
            data['name'] =  self._data.get('nvt')['name']
        
        return "{name} | {host} | {port} | {threat} | {severity}".format(**data)


class Note(OpenvasObject):
    """ Notes are associated with specific NVTs and generally scan results """
    text = field.Text().required()
    hosts = field.Text()
    category = field.Text()
    nvt = field.Object(Nvt)
    tags = field.Object()

class Override(OpenvasObject): pass