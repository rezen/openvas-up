""" Quick way to start scans """
from asset import Target
from secinfo import Config
from config import Scanner, Schedule
from scan import Task, Result
from meta import Tag

class ScanWizard(object):
    """ Creates a wizard for quickly starting up a scan task """

    def __init__(self, options={}):
        self.options = options if options is not None else {}
        self.host = None
        self.config = None
        self.messages = []
        self.target = None
        self.task_vas = None
        self.task_cve = None
        self.max_scan_time = 0 # time is in minutes
        self.is_complete = False
        self._results = None

    def start(self, options):
        """ Starts task creation process and validates options """
        self.host = options.get('host')
        self.config = options.get('config', 'Full and fast ultimate')

        if self.host is None:
            raise Exception('Required a host to start scan wizard')

        self.target = self._create_target(self.host)
        self.task_vas = self._create_task(self.target, 'OpenVAS')
        self.task_cve = self._create_task(self.target, 'CVE')

        self.task_vas.start()

    def results(self):
        if self._results is None:
            self._results = Result.get_for_task(self.task_vas) + Result.get_for_task(self.task_cve) 
        return self._results

    def wait_for_tasks(self):
        self._log("Waiting for OpenVAS scan")
        self.task_vas.reload()
        self.task_vas.wait_to_complete()
        
        self._log("Waiting for CVE scan")
        self.task_cve.reload()
        self.task_cve.wait_to_complete()
        self.is_complete = True

    def _create_task(self, target, scanner='OpenVAS'):
        config = [c for c in Config.get() if c.name == self.config].pop()
        scanner = [c for c in Scanner.get() if scanner in c.name].pop()

        name = 'Scan %s [%s] %s' % (target.hosts, config.name, scanner.name)
        tasks = Task.get_by_name(name)
        match = None

        try:
            match = [t for t in tasks if t.name == name].pop()
        except:
            pass

        if match is not None:
            self._log('Stopping, existing task with same name task_id=%s' % match.id)
            return match
        
        task = Task.from_dict({})
        task.name = name
        task.comment = 'Created by wizard'
        task.scanner = scanner
        task.target = target
        task.config = config
        task.save()

        try:
            self._tag_obj(task)
        except:
            pass

        self._log('Created task_id=%s name=%s' % (task.id, task.name))
        return task

    def _create_target(self, host):
        targets = Target.get_by_host(host)
        target = None
    
        if targets:
            targets = [t for t in targets if t.name == host]
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
            self._log('Created new target_id=%s' % target.id)
        else:
            self._log('Using existing matching target_id=%s name=%s' % (target.id, target.name))

        return target

    def _tag_obj(self, obj):
        tag = Tag.create_with_attach(obj)
        tag.name = 'FromWizard'
        tag.value = '1'
        tag.save()

    def _log(self, message=''):
        self.messages.append(message)


