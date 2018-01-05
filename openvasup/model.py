""" Base model """
from __future__ import print_function
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element
import field
import oxml
from util import ObservableDict, to_entity, omp_filter_from_dict
from omp import OmpConnection

def trim_tag(obj):
    if isinstance(obj, dict):
        if '$tag' in obj:
            del obj['$tag']
        return {k: trim_tag(obj[k]) for k in obj}
    elif isinstance(obj, list):
        return [trim_tag(o) for o in obj]
    return obj


PER_PAGE = 2

class OpenvasObject(object):
    """
    OpenvasObject is the base model openvas entities extend
    to create their base interactions with the omp connection
    """

    conn = None
    readonly = False
    default_filter = {}
    name = field.Text().required()
    comment = field.Text()

    @classmethod
    def connect(cls, **kwargs):
        """ Initiate connection to omp """
        username = kwargs.get('username')
        password = kwargs.get('password')
        host = kwargs.get('host', '127.0.01')
        port = kwargs.get('port', 9390)

        conn = OmpConnection(host=host, port=port, username=username, password=password)
        conn.open(username, password)
        cls.conn = OpenvasObject.conn = conn

    @classmethod
    def get_entity(cls):
        """ Get the name of the entity """
        if not hasattr(cls, 'entity'):
            cls.entity = to_entity(cls)
        return cls.entity

    def __new__(cls, *args, **kwargs):
        d = {k:v for k, v in cls.__dict__.items()}
        cls.field_names = getattr(cls, 'field_names', [])
        cls.fields = getattr(cls, 'fields', [])
        cls.required = getattr(cls, 'required', [])

        for key, value in d.items():
            if isinstance(value, field.Field):
                value.name = key
                value.add_to_class(cls, key)

        obj = super(OpenvasObject, cls).__new__(cls)
        obj._from_base_class = type(obj) == OpenvasObject
        obj.required = getattr(cls, 'required', [])
        obj.field_names = getattr(cls, 'field_names', [])
        obj.fields = getattr(cls, 'fields', [])
        obj.readonly = cls.readonly
        return obj

    def __init__(self, data={}, connection=None):
        self._data = data if data is not None else {}
        self._prev = {}
        self.conn = connection if connection is not None else self.__class__.conn
        self.entity = to_entity(self)
        self._dirty = set()
        self.is_creating = False
        self.is_modifying = False

    def get_editable(self):
        """ Get the names of the editable fields """
        return [f.name for f in self.fields if f.editable]

    @classmethod
    def from_xml(cls, xml):
        """ Create the model from xml """
        data = oxml.xml_to_dict(xml)
        return cls.from_dict(data)

    def to_xml(self, is_child=False):
        """ Convert the model to xml to be sent back to omp """
        if is_child is True:
            if self.id is None or self.id == '':
                return None
            return etree.Element(self.entity, {'id': str(self.id)})

        data = {name: getattr(self, name) for name in self.field_names}
        data = {k: v.to_xml(True) if hasattr(v, 'to_xml') else v for k, v in data.items() if v != None}
        elements = {k: oxml.knode(k, v) if k[0] != '@' else v for k, v in data.items() if v != None}

        if self.id is not None:
            elements['@%s_id' % self.entity] = self.id
        return elements

    def get_attr(self, attr):
        """ Get the model attribute """
        return self._data.get(attr)

    @property
    def id(self):
        """ Get the uuid of the model """
        return self._data.get('@id')

    @classmethod
    def from_dict(cls, data):
        """ Create a new instance of a model from a dict, resetting the dirty flags """
        instance = cls(data, cls.conn)
        for attr, value in data.items():
            setattr(instance, attr, value)

        instance._dirty = set()
        return instance

    @classmethod
    def get(cls, query=None):
        """ Get instances of the model with a query """
        query = query if query is not None else cls.default_filter
        entity = to_entity(cls)

        if '@filter' not in query:
            query['@filter'] = {}

        if isinstance(query['@filter'], dict):
            query['@filter']['rows'] = PER_PAGE
            query['@filter'] = omp_filter_from_dict(query['@filter'])
        elif isinstance(query['@filter'], basestring):
            query['@filter'] += " rows=%s" % PER_PAGE

        request = cls.conn.command('get_%ss' % entity, query)
        # @todo add in improved paging
        try:
            total = request.response_xml.find("%s_count" % entity)
            total = int(total.text)
        except:
            pass

        if hasattr(cls, 'from_xml'):
            entities = request.response_xml.findall(entity)
            return [cls.from_xml(e) for e in entities]

        return [cls.from_dict(t) for t in request.get_response_data()]

    @classmethod
    def get_by_id(cls, entity_id):
        """ Get a new instance of an entity by a specific uuid """
        query = {'@%s_id' % to_entity(cls): entity_id}
        return next(iter(cls.get(query) or []), None)

    
    def to_json(self):
        data = dict(self._data)
        for k, v in data.items():
            if v is None:
                continue
            if hasattr(v, 'to_json'):
                data[k] = v.to_json()
        return trim_tag(data)


    def to_dict(self, is_child=False):
        """ Convert model to dict, usually used for copying """
        if is_child:
            return {'@id': self.id}

        if len(self.field_names) != 0:
            data = {name: getattr(self, name) for name in self.field_names}
            data = {k: v.to_dict(True)  if hasattr(v, 'to_dict') else v for k, v in data.items()}
        else:
            data = self._data

        if self.id is not None:
            data['@%s_id' % self.entity] = self.id

        return data

    def changed_attrs(self):
        """ Get the names of the attributes that have changed  """
        fields = [(name, getattr(self, name)) for name in self.field_names]
        fields = set([k for (k, f) in fields if f != None and hasattr(f, 'changed') and f.changed])
        return fields.union(self._dirty)

    def has_changed(self):
        """ Check if the model has had any attribute changes """
        return len(self.changed_attrs()) != 0

    def save(self, **kwargs):
        """ Save the model, creating if it doesn't existing, modifying if it already does """
        if self.readonly:
            raise Exception('Cannot modify [%s] - entity is readonly' % self.entity)
        options = kwargs.copy()
        if self.id is not None:
            self.is_modifying = True
            value = self._modify(options)
            self.is_modifying = False
            return value
        self.is_creating = True
        value = self._create(options)
        self.is_creating = False
        return value

    def delete(self, ultimate=False):
        """ Delete the model, by default putting into trash, not permanent """
        return self.command('delete_' + to_entity(self), {
            '@%s_id' %  to_entity(self): self.id,
            '@ultimate': ultimate,
        })

    def copy(self):
        """ Create a new copy of the model's data """
        id_attr = '@' + to_entity(self) + 'id'
        data = self.to_dict().copy()
        cls = type(self)

        if 'copy' in self.field_names:
            pass

        if id_attr in data:
            del data[id_attr]

        if '@id' in data:
            del data['@id']

        if 'id' in data:
            del data['id']

        if 'name' in data:
            data['name'] = 'Copy - ' + data['name']

        return cls.from_dict(data)

    def command(self, name, details=None):
        """ Run a command against omp """
        if self.conn is None:
            raise Exception('There is no connection made yet, did you connect')

        details = details if details is not None else {}
        return self.conn.command(name, details)

    def _modify(self, options):
        if hasattr(self, 'modify') and callable(self.modify):
            return self.modify()

        command = 'modify_%s' % to_entity(self)
        payload = self.to_xml()
        editable = self.get_editable()

        if not self.has_changed() and 'force' not in options:
            print('nothin-changed')
            # @todo logger
            return

        if not isinstance(payload, dict):
            print('FIXME')
            exit(4)

        dirty = self.changed_attrs()
        payload = self._command_dict_xml(command, payload, dirty.union(set(editable)))
        request = self.command(command, payload)

        if not request.was_successful():
            raise Exception(request.status_text())
        
        return request.was_successful()
    
    def validate(self, payload):
        missing = [f for f in self.required if f not in payload]
        # @todo need a legit validator
        if len(missing) > 0:
            raise Exception("Missing attributes - %s" % ','.join(missing))

    def _create(self, options):
        if hasattr(self, 'create') and callable(self.create):
            return self.create(options)

        command = 'create_%s' % to_entity(self)
        payload = self.to_xml()
        self.validate(payload)
        payload = self._command_dict_xml(command, payload)

        request = self.command(command, payload)

        if request.was_successful():
            self._data['@id'] = request.get_id()
            return self._data['@id']


    def _command_dict_xml(self, command, data, attrs=None):
        xml = etree.Element(command)
        for key, elem in data.items():
            if isinstance(elem, tuple):
                attr, value = elem
                xml.attrib[attr] = value
            elif isinstance(elem, etree.Element):
                if attrs is None:
                    xml.append(elem)
                elif key in attrs:
                    xml.append(elem)
            elif key[0] == '@':
                xml.attrib[key[1:]] = elem
            else:
                pass
        return xml

    def __repr__(self):
        return "%s [id=%s name=%s]" % (self.__class__, self.id, self.name)
