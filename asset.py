""" Asset & host related models """
import re
from model import OpenvasObject
import field
from meta import Tag

class Target(OpenvasObject):
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
        query = {'@filter':'hosts=%s' % host}
        return super(Target, cls).get(query)


class Asset(OpenvasObject):
    name = field.Text().required()
    type = field.Text().required()
    comment = field.Text()
    user_tags = field.Object(Tag)
    in_use = field.Text()
    writable = field.Text()

    default_filter = {'@type':'host'}
    loose_ip_pattern = re.compile("^[0-9\.]+$")

    @classmethod
    def get_by_host(cls, host=None):
        if isinstance(host, list):
            filter = 'oss=%s'  % ','.join(host)
        elif isinstance(host, str):
            if cls.loose_ip_pattern.match(host):
                filter = 'ip=%s' % host
            else:
                filter = 'hostname=%s' % host
        query = {'@type':'host', '@filter':filter}
        return super(Asset, cls).get(query)

    @classmethod
    def get_by_os(cls, os_name=None):
        return super(Asset, cls).get({'@type':'os'})

    @classmethod
    def create_from_report(cls):
        pass


class PortList(OpenvasObject):
    entity = 'port_list'
    name = field.Text().required()
    comment = field.Text()
    port_range = field.TextCsv()
    writable = field.Text()

class PortRange(OpenvasObject):
    entity = 'port_range'
    port_list = field.Object(PortList)
    start = field.Integer()
    end = field.Integer()

