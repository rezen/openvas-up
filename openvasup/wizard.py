""" Quick way to start scans """
from asset import Target
from secinfo import Config
from config import Scanner, Schedule
from scan import Task
from meta import Tag

class ScanWizard(object):
    """ Creates a wizard for quickly starting up a scan task """

    def __init__(self, options={}):
        self.options = options if options is not None else {}
        self.host = None
        self.config = None
        self.messages = []
        self.target = None
        self.task = None
        self.max_scan_time = 0 # time is in minutes

    def start(self, options):
        """ Starts task creation process and validates options """
        self.host = options.get('host')
        self.config = options.get('config', 'Discovery')

        if self.host is None:
            raise Exception('Required a host to start scan wizard')

        self.target = self._create_target(self.host)
        self.task = self._create_task(self.target)

    def _create_task(self, target):
        config = [c for c in Config.get() if c.name == self.config].pop()
        name = 'Scan %s [%s]' % (target.hosts, config.name)
        tasks = Task.get_by_name(name)
        match = None

        try:
            match = [t for t in tasks if t.name == name].pop()
        except:
            pass

        if match is not None:
            self.messages.append('Stopping, existing task with same name task_id=%s' % match.id)
            return
        
        
        task = Task()
        task.name = name
        task.comment = 'Created by wizard'
        task.target = target
        task.config = config
        task.save()

        try:
            self._tag_obj(task)
        except:
            pass

        task.start()
        self.messages.append('Created and started task_id=%s name=%s' % (task.id, task.name))
        return task

    def _create_target(self, host):
        targets = Target.get_by_host(host)
        target = None
    
        if len(targets) > 0:
            target = targets.pop()
    
        if target is None:
            target = Target()
            target.name = host
            target.comment = 'Created by wizard'
            target.hosts = host
            # target.alive_tests = 'ICMP, TCP-ACK Service & ARP Ping'
            target.save()
            self._tag_obj(target)
            self.messages.append('Created new target_id=%s' % target.id)
        else:
            self.messages.append('Using existing matching target_id=%s' % target.id)

        return target

    def _tag_obj(self, obj):
        tag = Tag.attach(obj)
        tag.name = 'FromWizard'
        tag.value = '1'
        tag.save()

