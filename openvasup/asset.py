""" Asset & host related models """
import re
from model import OpenvasObject
import field
from meta import Tag
import oxml

class Target(OpenvasObject):
    """
    A target is a set of scannable resources
    with configured credentials, port_lists, etc
    """
    name = field.Text().required()
    comment = field.Text()
    hosts = field.Text().required()
    exclude_hosts = field.Text()
    reverse_lookup_only = field.Text()
    reverse_lookup_unify = field.Text()
    alive_tests = field.Text()
    port_range = field.Text()
    port_list = field.Object()

    @classmethod
    def get_by_host(cls, host=None):
        """ Get targets by the host identifier """
        query = {'@filter':'hosts=%s' % host}
        return super(Target, cls).get(query)


class Asset(OpenvasObject):
    """ Assets are added by scans generally and are tracked as a host and/or os """
    name = field.Text(editable=False).required()
    type = field.Text(editable=False).required()
    comment = field.Text()
    user_tags = field.Object(Tag)
    in_use = field.Text(editable=False)
    writable = field.Text(editable=False)

    default_filter = {'@type': 'host'}
    loose_ip_pattern = re.compile("^[0-9\.]+$")

    def validate(self, payload):
        # @todo
        pass

    def to_xml(self, is_child=False):
        if self.is_creating is True:
            data = super(Asset, self).to_xml(is_child).values()
            xmld = oxml.xnode('asset', *data)
            return {'asset': xmld}
        return super(Asset, self).to_xml(is_child)

    @classmethod
    def get_by_id(cls, entity_id, asset_type='host'):
        """ Get a new instance of an entity by a specific uuid """
        query = {'@asset_id': entity_id, '@type': asset_type}
        result = cls.get(query)
        return next(iter(result or []), None)

    @classmethod
    def get_by_host(cls, host=None):
        """ Get assets by host, either ip form or hostname """
        if isinstance(host, list):
            host = 'oss=%s' % ','.join(host)
        elif isinstance(host, str):
            if cls.loose_ip_pattern.match(host):
                host = 'ip=%s' % host
            else:
                host = 'hostname=%s' % host
        query = {'@type':'host', '@filter':host}
        return super(Asset, cls).get(query)

    @classmethod
    def get_by_os(cls, os_name=None):
        """ Get assets by os """
        return super(Asset, cls).get({'@type':'os'})

    @classmethod
    def create_from_report(cls, report):
        """ From a provided report, add the assets """
        pass

    def get_resource_type(self):
        """ Other resources, such as tags need correct resource type """
        return self._data['type']


class PortList(OpenvasObject):
    """ A configuration for what ports to scan """
    entity = 'port_list'
    name = field.Text().required()
    comment = field.Text()
    port_range = field.TextCsv()
    writable = field.Text()

class PortRange(OpenvasObject):
    """ A set of port lists """
    entity = 'port_range'
    port_list = field.Object(PortList)
    start = field.Integer()
    end = field.Integer()
