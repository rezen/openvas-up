""" All xml related utils live here """
from __future__ import print_function
from xml.etree import ElementTree as etree

def knode(key, value):
    """ Create a xml node based on a key, value pair """
    if isinstance(value, etree.Element):
        return value

    if isinstance(value, str):
        node = etree.Element(key)
        node.text = value
    elif isinstance(value, dict):
        return dict_to_xml(key, value)
    elif isinstance(value, list):
        pass
    return node

def xnode(tag, *kids, **attrs):
    """ Create an XML node ... """
    node = etree.Element(tag, attrs)
    for k in kids:
        if isinstance(k, str):
            assert node.text is None
            node.text = k
        else:
            node.append(k)
    return node

def dict_to_xml(name, data):
    """ Convert a dictionary to an XML structure """
    # @todo list handlings

    if hasattr(data, 'to_xml'):
        return data.to_xml()

    attrs = {}
    kids = []
    for key in data:
        value = data[key]
        if value is None:
            value = ''

        if isinstance(value, list):
            elements = [dict_to_xml(i['$tag'], i) for i in value]
            for el in elements:
                kids.append(el)
            continue

        if value == False or value == True:
            value = str(value).lower()

        if key[0] == '@':
            attrs[key[1:]] = value
            continue
        elif key == '$':
            kids.append(value)
            continue
        elif key == '$tag':
            name = value
            continue

        if isinstance(value, dict):
            kids.append(dict_to_xml(key, value))
        else:
            kids.append(xnode(key, value))
    return xnode(name, *kids, **attrs)

def print_xml(xml):
    """ Debug xml tool """
    print(xml)
    print(etree.tostring(xml, method='xml'))


def xml_to_dict(element, parent_tag=None):
    """ Convert an xml element to a dict """
    entry = {'$tag':element.tag}
    children = []

    if element.text is not None:
        entry['$text'] = element.text

    for elem in element:
        if len(elem) > 0:
            if parent_tag == (elem.tag + 's'):
                data = xml_to_dict(elem, elem.tag)
                data['$tag'] = elem.tag
                children.append(data)
            else:
                entry[elem.tag] = xml_to_dict(elem, elem.tag)
        else:
            # print('set %s' % elem.tag)
            if elem.tail is not None:
                entry['$tail'] = elem.tail
                entry[elem.tag] = (elem.text, elem.tail)
            else:
                entry[elem.tag] = elem.text
    if len(children) > 0:
        entry[parent_tag] = children

    for attr in element.attrib:
        entry['@' + attr] = element.attrib[attr]
    return entry
