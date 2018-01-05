""" Connector for omp """
from __future__ import print_function
import socket
import ssl
# @todo compat for python versions
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import XMLParser
import oxml

MANAGER_ADDRESS = '127.0.0.1'
MANAGER_PORT = 9390
socket.setdefaulttimeout(7)

class Error(Exception):
    """Base class for OMP errors."""
    def __str__(self):
        return repr(self)

class AuthFailedError(Error):
    """Authentication failed."""

class ResultError(Error):
    """Get invalid answer from Server"""

class ClientError(Error):
    """ Error in how client is used """

class NotFoundError(Error):
    """ Error if result not found """

"""
class OpenvasConnection:
    def __init__(self, host, port=MANAGER_PORT, username=None, password=None):
        self.socket = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.session = None
    
    def open(self, username=None, password=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = sock = ssl.wrap_socket(sock,do_handshake_on_connect=False)
        print(self.host, self.port)
        sock.connect((self.host, self.port))
        self.authenticate(username, password)

    def close(self):
        self.socket.close()
        self.socket = None
"""

class Request:
    def __init__(self, name, data):
        self.command = name
        self.data = data
        self.response_body = ''
        self.response_xml = None
        self.method, self.resource = self.command_parts(name)
        self._dict = None

    def set_response(self, (xml, body)):
        """ Set the response attributes """
        self.response_body = body
        self.response_xml = xml

    def get_response_data(self):
        """ Get the data from the response """
        data = self.response_to_dict()
        resource = data.get(self.resource, data)
        if resource is None:
            return []
        else:
            return resource

    def get_status_text(self):
        """ Get the status text returned from omp response """
        return self.response_xml.attrib['status_text']

    def get_status_code(self):
        """ Get the status code returned from omp response """
        return int(self.response_xml.attrib['status'])

    def command_parts(self, command):
        """ Get the method and resource from the command """
        parts = command.split("_")
        method = parts[0]
        resource = '_'.join(parts[1:])
        return method, resource

    def get_id(self):
        """ Get the id in the response """
        return self.response_xml.attrib['id']

    def was_successful(self):
        """ Returns whether or not the request succeeded """
        return self.get_status_code() < 300

    def response_to_dict(self):
        """ Conver the response to a dict """
        if self._dict is None:
            self._dict = oxml.xml_to_dict(self.response_xml, self.resource)
        return self._dict

class OmpConnection:
    """ Does the stuff ... """
    def __init__(self, host, port=MANAGER_PORT, username=None, password=None):
        self.socket = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.session = None
        self._is_authed = False

    def open(self, username=None, password=None):
        """ Opens up with connection with omp """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = sock = ssl.wrap_socket(sock, do_handshake_on_connect=False)
        sock.connect((self.host, self.port))
        self.authenticate(username, password)

    def authenticate(self, username=None, password=None):
        """ Sends authenticate command to omp """
        if self._is_authed and username is None:
            return

        if username is None:
            username = self.username
        if password is None:
            password = self.password

        request = self.command('authenticate', {
            'credentials':{
                'username':username,
                'password':password
            }
        })

        if not request.was_successful():
            raise AuthFailedError(request.get_status_text())

        self._is_authed = True

    def close(self):
        """ Close the connection out """
        self.socket.close()
        self.socket = None
        self._is_authed = False

    def send_xml(self, data):
        """ Send xml data """
        if not etree.iselement(data):
            raise ClientError('Not xml ...')

        root = etree.ElementTree(data)
        root.write(self.socket, 'utf-8')
        return self._receive()

    def send_dict(self, data): pass

    def send_text(self, data):
        """ Send raw text to connection """
        if not isinstance(data, unicode):
            raise ClientError('Not text ...')

        data = data.encode('utf-8')
        self.socket.send(data)
        return self._receive()

    def _receive(self):
        BLOCK_SIZE = 1024
        parser = XMLParser()
        body = ""
        while 1:
            res = self.socket.recv(BLOCK_SIZE)
            parser.feed(res)
            body += res
            if len(res) < BLOCK_SIZE:
                break
        root = parser.close()
        return (root, body)

    def send(self, data):
        """ Send data to connection """
        if isinstance(data, unicode):
            return self.send_text(data)
        elif isinstance(data, dict):
            return self.send_dict(data)
        elif etree.iselement(data):
            return self.send_xml(data)
    
    def command_dict(self, name, data):
        """ Send a command name with params stored in dict """
        request = Request(name, data)
        xmld = oxml.dict_to_xml(name, data)
        request.set_response(self.send_xml(xmld))
        return request

    def command_xml(self, name, data):
        """ Send a command name with request xml built """
        request = Request(name, data)
        request.set_response(self.send_xml(data))
        return request
    
    def help(self):
        """ Get help info from omp """
        request = self.command('help', {})
        if request.was_successful():
            return request.response_xml.text

    def command(self, name, data):
        """ Send a command in format of command name and dictionary and convert to xml """
        if isinstance(data, dict):
            request = self.command_dict(name, data)
        else:
            request = self.command_xml(name, data)

        if not request.was_successful():
            if request.get_status_code() == 404:
                raise NotFoundError('Command failed [' + name + '] ' + request.get_status_text())
            else:
                raise ResultError('Command failed [' + name + '] ' + request.get_status_text())

        return request
