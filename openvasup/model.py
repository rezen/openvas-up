""" Base model """
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element
import field
import oxml
from util import ObservableDict, to_entity
from omp import OmpConnection

class OpenvasObject(object):
    """ @todo """
    conn = None
    readonly = False
    default_filter = {}
    name = field.Text().required()
    comment = field.Text()

    @classmethod
    def connect(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        host = kwargs.get('host', '127.0.01')
        port = kwargs.get('port', 9390)

        conn = OmpConnection(host=host, port=port, username=username, password=password)
        conn.open(username, password)
        cls.conn = OpenvasObject.conn = conn

    @classmethod
    def get_entity(cls):
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
    
    def get_editable(self):
        return [f.name for f in self.fields if f.editable]

    @classmethod
    def from_xml(cls, xml):
        data = oxml.xml_to_dict(xml)
        return cls.from_dict(data)

    def to_xml(self, is_child=False):
        if is_child is True:
            if self.id is None or self.id == '':
                return None
            return etree.Element(self.entity, {'id': str(self.id)})

        data = {name: getattr(self, name) for name in self.field_names}
        data = {k:v.to_xml(True) if hasattr(v, 'to_xml') else v for k, v in data.items() if v != None}
        elements = {k: oxml.knode(k, v) if k[0] != '@' else v for k, v in data.items() if v != None}

        if self.id is not None:
            elements['@%s_id' % self.entity] =  self.id
        return elements
    
    def get_attr(self, attr):
        return self._data.get(attr)

    @property
    def id(self):
        """ @todo """
        return self._data.get('@id')

    @classmethod
    def from_dict(cls, data):
        """ @todo """
        instance = cls(data, cls.conn)
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance._dirty = set()
        return instance

    @classmethod
    def get(cls, query=None):
        """ @todo """
        query = query if query is not None else cls.default_filter
        entity = to_entity(cls) 
        request = cls.conn.command('get_%ss' % entity, query)
        
        if hasattr(cls, 'from_xml'):
            entities = request.response_xml.findall(entity)
            return [cls.from_xml(e) for e in entities]
    
        return [cls.from_dict(t) for t in request.get_response_data()]
    
    @classmethod
    def get_by_id(cls, entity_id):
        """ @todo """
        query = {'@%s_id' % to_entity(cls):entity_id}
        return next(iter(cls.get(query) or []), None)

    def to_dict(self, is_child=False):
        if is_child == True:
            return {'@id':self.id}

        if len(self.field_names) != 0:
            data = {name:getattr(self, name) for name in self.field_names}
            data = {k:v.to_dict(True)  if hasattr(v, 'to_dict') else v for k, v in data.items()}
        else:
            data = self._data

        if self.id is not None:
            data['@%s_id' % self.entity ] = self.id
        
        return data
    
    def changed_attrs(self):
        fields = [(name, getattr(self, name)) for name in self.field_names]
        fields = set([k for (k, f) in fields if f is not None and hasattr(f, 'changed') and f.changed == True])
        return fields.union(self._dirty)

    def has_changed(self):
        return len(self.changed_attrs()) != 0
    
    def save(self, **kwargs):
        """ @todo """
        if self.readonly:
            raise Exception('Cannot modify [%s] - entity is readonly' % self.entity)
        options = kwargs.copy()
        if self.id is not None:
            return self._modify(options)

        return self._create(options)
    
    def delete(self, ultimate=False):
        """ @todo """
        return self.command('delete_' + to_entity(self), {
            '@%s_id' %  to_entity(self): self.id,
            '@ultimate': ultimate,
        })
    
    def copy(self):
        """ @todo """
        id_attr = '@' + to_entity(self) + 'id'
        data =  self.to_dict().copy()
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
        """ Comment here """
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
        response = self.command(command, payload)

    def _create(self, options):
        if hasattr(self, 'create') and callable(self.create):
            return self.create()

        command = 'create_%s' % to_entity(self)
        payload = self.to_xml()
        missing = [f for f in self.required if f not in payload]
        payload = self._command_dict_xml(command, payload)

        # @todo need a legit validator
        if len(missing) > 0:
            raise Exception("Missing attributes - %s" % ','.join(missing))

        request = self.command(command, payload)

        if request.was_successful():
            self._data['@id'] = request.get_id()

    
    def _command_dict_xml(self, command, data, attrs=None):
        xml = etree.Element(command)
        for key, el in data.items():
            if isinstance(el, tuple):
                attr, value = el
                xml.attrib[attr] = value
            elif isinstance(el, etree.Element):
                if attrs is None:
                    xml.append(el)   
                elif key in attrs:
                    xml.append(el)        
            elif key[0] == '@':
                xml.attrib[key[1:]] = el
            else:
                pass
        return xml

    def __repr__(self):
        return "%s [id=%s name=%s]" % (self.__class__, self.id, self.name)



