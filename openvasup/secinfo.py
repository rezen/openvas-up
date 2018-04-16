""" Models related to nvt, cve, etc """
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element
from model import OpenvasObject
from util import ObservableList
from meta import Tag
import field
import oxml
import re
import pprint

pp = pprint.PrettyPrinter(indent=2)

def xml_parse_families(xml):
    return [(f.find('name').text, int(f.find('max_nvt_count').text)) for f in xml.findall('families/family')]

class NvtSelection(object):

    def __init__(self, name, max_nvt_count=-1, nvts=[], config_id=None):
        self.name = name
        self.max_nvt_count = max_nvt_count
        self.config_id = config_id
        self._is_loaded = False
        self.set_nvts(nvts if nvts is not None else [])
        self.use_all = False

    def set_nvts(self, nvts):
        self.nvts = ObservableList(nvts)
        return self
    
    def load_nvt_max(self):
        self.max_nvt_count = len(Nvt.get_by_family(self.name))

    def load_nvts_selected(self):
        if self.config_id is None:
            return self

        nvts = Nvt.get_config_family(self.name, self.config_id)
        self.set_nvts(nvts)
        self._is_loaded = True
        return self
    
    def select_all_nvts(self):
        self.use_all = True
        nvts = Nvt.get_by_family(self.name)
        self.max_nvt_count = len(nvts)
        self.set_nvts(nvts)

    def has_changed(self):
        return self.nvts.changed == True

    def has_any_selected(self):
        return len(self.nvts) > 0

    def has_all_selected(self):
        return (self.max_nvt_count <= len(self.nvts))

    def exclude_nvt(self, nvt):
        self.nvts = [n for n in self.nvts if n.get_attr('@oid') != nvt.get_attr('@oid')]
        self.nvts.changed = True

    def include_oid(self, oid):
        nvt = Nvt.from_dict({'@oid': oid})
        self.include_nvt(nvt)

    def include_nvt(self, nvt):
        matches = [n for n in self.nvts if n.get_attr('@oid') == nvt.get_attr('@oid')]
        if len(matches) > 0:
            return
        self.nvts.append(nvt)

    def to_xml_family(self):
        tree = etree.ElementTree(etree.fromstring("\n".join([
            "<family>",
            "  <name>%s</name>" % self.name,
            "  <nvt_count>%s</nvt_count>" % len(self.nvts),
            "  <max_nvt_count>%s</max_nvt_count>" % self.max_nvt_count, 
            "  <growing>1</growing>",
            "</family>",
        ])))
        return tree.getroot()

    def to_xml_all(self):
        tree = etree.ElementTree(etree.fromstring("\n".join([
            "<family_selection>",
            "  <family>",
            "    <name>%s</name>" % self.name,
            "    <all>1</all>",
            "    <growing>1</growing>",
            "  </family>",
            "</family_selection>"
        ])))
        return tree.getroot()

    def to_xml_selection(self):
        segments = ['<nvt_selection>', '  <family>%s</family>'% self.name]
        for nvt in self.nvts:
            segments.append('  <nvt oid="%s"/>' % nvt.get_attr('@oid'))
        segments.append('</nvt_selection>')
      
        tree = etree.ElementTree(etree.fromstring("\n".join(segments)))
        return tree.getroot()

    def to_xml(self):
        if self.has_all_selected():
            return self.to_xml_all()
         
        return self.to_xml_selection()

    def __repr__(self):
        return "%s [name=%s max_nvt_count=%s]" % (self.__class__, self.name, self.max_nvt_count)

    @classmethod
    def from_family_xml(cls, xml, config_id):
        return cls(xml.find('name').text, int(xml.find('max_nvt_count').text), [], config_id)


class Nvt(OpenvasObject):
    """ Network vulnerability test """
    name = field.Text()
    category = field.Text()
    default_filter = {'@details':'1'}

    @classmethod
    def get_by_family(cls, family):
        return cls.get({
            '@sort_field': 'name',
            '@family': family,
        })


    def to_xml_selector(self):
        xml = oxml.dict_to_xml('nvt_selector', {
            # 'name': self.name,
            'include': self.get_attr('include', '1'),
            'type': self.get_attr('type', '2'),
            'family_or_nvt': self.get_attr('@oid'),
        })
        return xml

    @classmethod
    def get_config_family(cls, family, config_id):
        return cls.get({
            '@family': family,
            '@config_id': config_id
        })

    @classmethod
    def get_families(cls):
        request = cls.conn.command('get_nvt_families', {})
        xml = request.response_xml
        return [f for f in xml.findall('families/family')]

    @classmethod
    def get_by_config(cls, config_id):
        """ The omp protocol appears to be broken """
        request = cls.conn.command('get_nvt_families', {})
        xml = request.response_xml

        # @todo don't group by family?
        return [NvtSelection.from_family_xml(f, config_id) for f in xml.findall('families/family')]


class ConfigPreference(object): 
    def __init__(self, data):
        self.name = data.get('name')
        self.value = data.get('value')
        self.default = data.get('default')
        self.nvt_oid = data.get('nvt_oid')
    
    def is_not_default(self):
        if self.value == "" or self.value is None:
            return False
        return self.value != self.default
    
    def is_for_nvt(self):
        return self.nvt_oid != None and len(self.nvt_oid) >= 2

    def to_xml(self, _is_child=False):
        """ Convert instance to xml """
        data = {'name': self.name, 'value': str(self.value)}
        if self.is_for_nvt():
            data['nvt'] = {'@oid': self.nvt_oid}
    
        return oxml.dict_to_xml('preference', data)

    def __repr__(self):
        return "%s [name=%s value=%s oid=%s]" % (self.__class__, self.name, self.value, self.nvt_oid)

    @classmethod
    def from_xml(cls, xml):
        instance = cls({
            'nvt_oid':xml.find('nvt').attrib.get('oid'),
            'name':xml.find('name').text,
            'hr_name':xml.find('hr_name').text,
            'type':xml.find('type').text,
            'value':xml.find('value').text,
            'default':xml.find('default').text,
        })
        instance._source = xml
        return instance

class Config(OpenvasObject):
    """ For configuring details of a scan """
    comment = field.Text()
    name = field.Text()

    @classmethod
    def get_by_id(cls, entity_id):
        """ Get a new instance of an entity by a specific uuid """
        query = {
            '@config_id' : entity_id,
            '@details': 1,
            '@families': 1,
        }
        return next(iter(cls.get(query) or []), None)

    @classmethod
    def get_by_name(cls, name):
        query = {
            '@filter': 'name="%s"' % name,
            '@details': 1,
            '@families': 1,
        }
        return next(iter(cls.get(query) or []), None)

    def is_global(self):
        return self.get_attr('owner') == None and len(self.permissions) == 0

    def update_selection(self, selection, force=False):
        if not selection.has_changed() and force == False:
            return

        node = etree.Element('modify_config')
        node.attrib['config_id'] = self.id
        node.append(selection.to_xml())
        request = self.command('modify_config', node)

    def update_preference(self, preference):
        node = etree.Element('modify_config')
        node.attrib['config_id'] = self.id
        node.append(preference.to_xml())
        request = self.command('modify_config', node)

    def modify(self, force=False):
        if self.get_attr('in_use') == '1':
            raise Exception("You cannot modify a scan config already in use")

        for selection in self.get_attr('selections'):
            self.update_selection(selection, force)
        
        preferences = self.get_attr('preferences')
        if preferences.changed == True or force == True:
            [self.update_preference(p) for p in preferences]
        

    def export(self, path):
        request = self.command('get_configs', {
            '@config_id': self.id,
            '@details': 1,
            '@families': 1,
        })
        with open(path, "w") as handle:
            handle.write(request.response_body)
    
    def add_preference(self, preference): pass

    @classmethod
    def imports(cls, xml_path):
        # @todo check if name already exists
        config_data = ''
        with open(xml_path) as handle:
            config_data = handle.read()
        
        # @todo remove tags and make separate calls
        xml, body = cls.conn.send_text('<create_config>%s</create_config>' % config_data)
        
        if "201" not in body:
            raise Exception(body)
        
        id = xml.find('config').attrib.get('id')
        return cls.get_by_id(id)

    @classmethod
    def from_xml_preferences(cls, xml):
        preferences = []
        for pref in xml.findall('preferences/preference'):
            config_pref = ConfigPreference.from_xml(pref)
            if config_pref.is_not_default():
                preferences.append(config_pref)
        return ObservableList(preferences)

    def get_slug(self):
        pattern = re.compile('[^A-z0-9\-]+')
        double_dash = re.compile('[-]{2,}')
        slug = pattern.sub('', self.name.replace(' ', '-').lower())
        return double_dash.sub('-', slug)

    @classmethod
    def from_xml(cls, xml):
        """ Create instance from xml """
        tags = ObservableList([Tag.from_xml(t) for t in xml.findall('user_tags/tag')])

        data = {
            '@id' : xml.attrib.get('id'),
            'owner': xml.find('owner/name').text,
            'name': xml.find('name').text,
            'comment': xml.find('comment').text,
            'in_use': xml.find('in_use').text,
            'nvt_count': int(xml.find('nvt_count').text),
            'creation_time': xml.find('creation_time').text,
            'modification_time': xml.find('modification_time').text,
            'preferences': cls.from_xml_preferences(xml),
            'permissions': [p.text for p in xml.findall('permissions/permission')],
            'tags': ObservableList([Tag.from_xml(t) for t in xml.findall('user_tags/tag')]),
            'selections': []
        }

        data['selections'] = [NvtSelection.from_family_xml(f, data['@id']) for f in xml.findall('families/family')]
        data['selections'] = [s.load_nvts_selected() for s in data['selections']]
        return cls.from_dict(data)
