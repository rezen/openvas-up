from __future__ import print_function
import pprint
from sets import Set
from xml.etree import ElementTree as etree
import sys
sys.path.append("..")
from openvasup.model import OpenvasObject
from openvasup.meta import Tag
from openvasup.secinfo import Config, ConfigPreference, NvtSelection, Nvt
from openvasup.util import ObservableList
import openvasup.oxml as oxml
import uuid
import xml.etree.cElementTree as ET
import yaml
import tempfile

# Start openvas with Docker to get things doing quick!
# `docker run -d -p 443:443 -p 9390:9390 --name openvas mikesplain/openvas`
# PYTHONIOENCODING=UTF-8 python scan_config.py

class ScanConfigImporterYaml:
    def __init__(self, data={}):
        self.data = data
    
    def run(self):
        _, tmpfile = tempfile.mkstemp(prefix='openvas-scan-config-', suffix='.xml')

        self.to_xml(tmpfile)
        config = Config.imports(tmpfile)
        config.modify(force=True)

        for tag in self.data.get('tags'):
            tag.attach(config)
            tag.save()

    def to_xml(self, file_export):
        data = self.data
        selected = data.get('selected', [])
        config_node = etree.Element('config')
        root = etree.Element('get_configs_response')
        tags = etree.Element('user_tags')

        for tag in data.get('tags', []):
            tags.append(etree.fromstring('<tag><name>%s</name><value>%s</value></tag>' % (tag.name, tag.value)))

        config_node.append(tags)
        config_node.append(oxml.knode('name', data['name']))
        config_node.append(oxml.knode('type', '0'))
        config_node.append(etree.fromstring('<family_count>%s<growing>1</growing></family_count>' % len(selected)))
        config_node.append(oxml.dict_to_xml('nvt_count', {'growing': '1'}))

        nvts_selectors = etree.Element('nvt_selectors')
        families = etree.Element('families')
        for s in data.get('selections', []):
            families.append(s.to_xml_family())
            for nvt in s.nvts:
                nvts_selectors.append(nvt.to_xml_selector())
        
        config_node.append(families)
        config_node.append(nvts_selectors)

        preferences = etree.Element('preferences')
        for pref in data['preferences']:
            preferences.append(pref.to_xml())
        
        config_node.append(preferences)
        root.append(config_node)
        tree = ET.ElementTree(root)
        tree.write(file_export)
    
    @classmethod
    def _parse_preferences(cls, data):
        return [ConfigPreference(p) for p in data.get('preferences', [])]

    @classmethod
    def _parse_tags(cls, data):
        return [Tag.from_dict(p) for p in data.get('tags', [])] + [Tag.from_dict({'name': 'import_src', 'value': 'yaml'})]

    @classmethod
    def _parse_selections(cls, data):
        selected = []
        for family in data.get('families'):
            nvts = family.get('nvts', [])
            nvts = nvts if nvts is not None else []
            selection = NvtSelection(family['family'])

            if family.get('all', False):
                selection.select_all_nvts()
            else:
                [selection.include_oid(oid) for oid in nvts]
                selection.load_nvt_max()

            selected.append(selection)
        return selected

    @classmethod
    def from_data(cls, data):
        data['preferences'] = cls._parse_preferences(data)
        data['tags'] =  cls._parse_tags(data)
        data['selections'] = cls._parse_selections(data)
        del data['families']
        return cls(data)

    @classmethod
    def from_yaml(cls, yaml_file):
        data = {}
        with open(yaml_file, 'r') as handle:
            try:
                data = yaml.load(handle) 
            except yaml.YAMLError as exc:
                print(exc)
     
        return cls.from_data(data)


class ScanConfigYamlExporter:
    def __init__(self): pass

    def _append_families(self, text):
        text.append("families:")
        for selection in self.config.get_attr('selections'):
            text.append("  - family: '%s'" % selection.name)
        
            if not selection.has_all_selected():
                text.append("    nvts: ")
                for nvt in selection.nvts:
                    text.append("      - '%s'" % nvt.get_attr('@oid'))
            else:
                text.append("    all: true")
            text.append("")
        return text

    def _append_prefs(self, text):
        text.append("preferences:")
        for preference in self.config.get_attr('preferences'):
            text.append("  - name: '%s'" % preference.name)
            text.append("    value: '%s'" % preference.value)
            text.append("    type: '%s'" % preference.get_attr('type'))

            if preference.is_for_nvt():
                text.append("    oid: '%s'" % preference.nvt_oid)
            text.append("")
        return text

    def _append_tags(self, text):
        text.append('tags:')
        for tag in self.config.get_attr('tags'):
            text.append("  - name: '%s'" % tag.name)
            text.append("    value: '%s'" % tag.value)
            text.append("    value: '%s'" % tag.comment if tag.comment != None else '')
            text.append("")
        return text

    def to_yaml(self):
        config = self.config
        text = ['---']
        text.append("name: '%s'" % config.name)
        text.append("comment: '%s'" % (config.comment if config.comment != None else ''))
        text = self._append_families(text)
        text = self._append_prefs(text)
        text = self._append_tags(text)
        return "\n".join(text)

def main():
    pp = pprint.PrettyPrinter(indent=2)
    username = 'admin'
    password = 'admin'
    OpenvasObject.connect(host='172.17.0.2', username=username, password=password)
    config = {}

    # config = Config.get_by_id('b07d451e-fe95-49b1-82ff-9803f32f7b69')
    # yamler = ScanConfigYamler(config)
    # print(yamler.to_yaml())
    importer = ScanConfigImporterYaml.from_yaml('confs/full-scans-linux.yaml')
    importer.run()
    # i3l   ()
    # Config.imports('conf-gen.xml')

if __name__ == "__main__":
    main()
