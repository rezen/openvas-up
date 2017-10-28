""" Config related models """
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element
import field
from model import OpenvasObject
from util import ObservableDict

class AlertCondition(object):
    """ Condition that event must fulfill to trigger alert """
    def __init__(self, event, name=None, value=None):
        self.event = event
        self.name = name
        self.value = value

    def to_xml(self, _is_child=False):
        """ Convert instance to xml """
        if self.name is None:
            tmpl = '<condition>{o.event}</condition>'
        else:
            tmpl = '<condition>{o.event}<data><name>{o.name}</name>{o.value}</data></condition>'

        tree = etree.ElementTree(etree.fromstring(tmpl.format(o=self)))
        return tree.getroot()

    @classmethod
    def from_xml(cls, xml):
        """ Create instance from xml """
        data = {'event':xml.text}

        if data['event'] == 'Always':
            pass
        else:
            data['name'] = xml.find('data/name').text
            data['value'] = xml.find('data/name').tail
        return cls(**data)

class AlertMethod(object):
    """ What kind of alert is fired off """
    methods = [
        'Email',
        'HTTP Get',
        'SCP',
        'Send',
        'SNMP',
        'Sourcefire Connector',
        'Start Task',
        'Syslog',
        'verinice Connector',
    ]

    def __init__(self, method, data={}):
        def _on_change():
            self.changed = True
        self.method = method
        self.data = ObservableDict(data, callback=_on_change)
        self.changed = False


    @staticmethod
    def is_valid_method(method):
        """ Is the name name a valid method? """
        return method in AlertMethod.methods

    def to_xml(self, _is_child=False):
        """ Convert instance to xml """
        xml = etree.Element('method')
        xml.text = self.method

        for key, value in self.data.items():
            data = etree.Element('data')
            name = etree.Element('name')
            name.text = key
            name.tail = value
            data.append(name)
            xml.append(data)
        return xml

    @classmethod
    def from_xml(cls, xml):
        """ Create instance from xml """
        data = {'method':xml.text, 'data':{}}
        for d in xml.findall('data'):
            key, value = [e for e in d.itertext()]
            data['data'][key] = value

        return cls(**data)


class AlertEvent(object):
    """ Event that triggers an alert """
    events = [
        'Task run status changed',
        'New SecInfo arrived',
        'Updated SecInfo arrived',
        'Internal Error'
    ]

    options = [
        # status
        'Done',
        'New',
        'Requested',
        'Running',
        'Stop Requested',
        'Stopped',
        # secinfo_type
        'nvt',
        'cve',
        'cpe',
        'cert_bund_adv',
        'dfn_cert_adv',
        'ovaldef',
    ]

    def __init__(self, event, name=None, value=None):
        if not AlertEvent.is_valid_event(event):
            raise Exception('invalid event '+ event)

        if name not in 'status|secinfo_type':
            raise Exception('invalid name')
        
        if not AlertEvent.is_valid_value(value):
            raise Exception('invalid valid')
    
        self.event = event   # 
        self.name = name
        self.value = value

    def to_xml(self, _is_child=False):
        """ Convert instance to xml """
        if self.name is None:
            tmpl = '<event>{o.event}</event>'
        else:
            tmpl = '<event>{o.event}<data><name>{o.name}</name>{o.value}</data></event>'

        tree = etree.ElementTree(etree.fromstring(tmpl.format(o=self)))
        return tree.getroot()
        
    
    @staticmethod
    def is_valid_event(event):
        """ Is the event a valid event name """
        return event in  AlertEvent.events

    @staticmethod
    def is_valid_value(value):
        """ Is the event value a valid name """
        return value in AlertEvent.options

    @classmethod
    def from_xml(cls, xml):
        """ Create instance from xml """
        data = {'event':xml.text}
        data['name'] = xml.find('data/name').text
        data['value'] = xml.find('data/name').tail
        return cls(**data)


class Alert(OpenvasObject):
    """ Alerts are actions triggered by specific events/conditions """
    name = field.Text()
    comment = field.Text()
    copy = field.Uuid()
    condition = field.Object(AlertCondition)
    event = field.Object(AlertEvent)
    method = field.Object(AlertMethod)
    filter = field.Object()

    @classmethod
    def from_xml(cls, xml):
        """ Create an alert instance from xml """
        return cls.from_dict({
            '@id':xml.attrib['id'],
            'name':xml.find('name').text,
            'comment':xml.find('comment').text,
            'condition':xml.find('condition'),
            'method': xml.find('method'),
            'event': xml.find('event'),
        })
 

class Credential(OpenvasObject):
    """ Credentials give authenticated access to targets """
    name = field.Text()
    comment = field.Text()
    login = field.Text()
    password = field.Text()
    community = field.Text()
    type = field.Text()

class Scanner(OpenvasObject):
    """ For distributing scan task workload """
    name = field.Text()
    comment = field.Text()
    host = field.Text()
    port = field.Text()
    type = field.Text()
    ca_pub = field.Text()

class Config(OpenvasObject):
    """ For configuring details of a scan """
    # omp?cmd=get_configs&token=39d92b71-0a5f-42a8-bc2c-dd85e98e8a46
    comment = field.Text()
    name = field.Text()

class Schedule(OpenvasObject):
    """ Frequency and/or timing of when a scan will happen """
    name = field.Text()
    comment = field.Text()
    first_time = field.Object()
    duration = field.Object()
    period = field.Object()
    timezone = field.Text()

class Agent(OpenvasObject):
    """ Magic sauce I don't understand ... """
    name = field.Text().required()
    comment = field.Text()
    installer = field.Base64().required()
    signature = field.Text()
    howto_use = field.Text()
    howto_install = field.Text()

    def to_xml(self, _is_child=False):
        """ Convert instance to xml """
        installer = etree.Element('installer')
        installer.text = self.installer
        sig = etree.Element('signature')
        sig.text = self.signature
        installer.append(sig)
        return {
            'name': self.name,
            'comment': self.comment,
            'installer': installer,
            'howto_use': self.howto_use,
            'howto_install': self.howto_install,
        }


    @classmethod
    def from_xml(cls, xml):
        """ Create instance from xml """
        return cls.from_dict({
            '@id':xml.attrib['id'],
            'name':xml.find('name').text,
            'comment':xml.find('comment').text,
            'installer': xml.find('installer').text,
            'signature': xml.find('installer/signature').text,
            'howto_use': xml.find('howto_use').text,
            'howto_install': xml.find('howto_install').text,
        })

class Preference(object): pass

class Setting(OpenvasObject):
    """ Settings for omp/openvas """
    name = field.Text(readonly=True).required()
    value = field.Text(readonly=True).required()