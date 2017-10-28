from __future__ import print_function
import pytest
import openvasup.oxml as oxml
from xml.etree import ElementTree as etree
import sys

class TestOxml:

    def test_dict_to_xml(self):
        xml = oxml.dict_to_xml('test', {'@id': 1})
        assert etree.tostring(xml, method='xml') == '<test id="1" />'

    def test_xml_to_dict(self):
        elem = etree.Element('test')
        elem.text = 'test'
        elem.attrib['name'] = 'alpha'
        data = oxml.xml_to_dict(elem)
        assert data == {'$tag': 'test', '$text': 'test', '@name': 'alpha'}

    def test_xml_dict_back(self):
        xml = oxml.dict_to_xml('create_agent', {'@id': '123-456-789'})
        data = oxml.xml_to_dict(xml)
        back = oxml.dict_to_xml(data['$tag'], data)
        assert etree.tostring(xml, method='xml') == etree.tostring(back, method='xml')
