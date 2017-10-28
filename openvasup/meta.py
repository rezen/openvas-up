""" Note, annotation related models """
from model import OpenvasObject
import field
from secinfo import Nvt


class Tag(OpenvasObject):
    """ Tag entities with extra data """
    name = field.Text()
    comment = field.Text()
    value = field.Text()
    resource = field.Object()
    active = field.Text()

    @staticmethod
    def attach(obj):
        """ Add tag to an object """
        tag = Tag({'@id': None})
        tag.resource = {
            '@id': obj.id,
            'type': obj.entity
        }
        return tag

class Note(OpenvasObject):
    """ Notes are associated with specific NVTs and generally scan results """
    text = field.Text().required()
    hosts = field.Text()
    category = field.Text()
    nvt = field.Object(Nvt)
    tags = field.Object()

class Override(OpenvasObject): pass