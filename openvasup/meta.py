""" Note, annotation related models """
from model import OpenvasObject
from util import omp_filter_from_dict
import field

class Tag(OpenvasObject):
    """ Tag entities with extra data """
    name = field.Text()
    comment = field.Text()
    value = field.Text()
    resource = field.Object()
    active = field.Text()

    def create_if_new(self):
        """ Create a tag if it doesn't already exist """
        if self.id is not None:
            # The tag has an id ... so it exists?
            return

        uuid = None if  self.resource is None else self.resource['@id']
        
        filter_string = omp_filter_from_dict({
            'resource_uuid': uuid,
            'name': self.name,
            'value': self.value,
        })
        tags = Tag.get({'@filter': filter_string})

        if len(tags) > 0:
            return

        return self.save()

    def attach(self, obj):
        if hasattr(obj, 'get_resource_type'):
            entity = obj.get_resource_type()
        else:
            entity = obj.entity

        self.resource = {
            '@id': obj.id,
            'type': entity
        }
        return self

    @classmethod
    def create_with_attach(cls, obj):
        """ Add tag to an object """
        tag = cls({'@id': None})
        return tag.attach(obj)
