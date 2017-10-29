""" Note, annotation related models """
from model import OpenvasObject
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

        uuid = self.resource['@id']
        # @todo improve for tags that are not associated with specific resources
        filter_string = 'resource_uuid=%s and name=%s and value=%s' % (uuid, self.name, self.value)
        tags = Tag.get({'@filter': filter_string})

        if len(tags) > 0:
            return

        return self.save()

    @staticmethod
    def attach(obj):
        """ Add tag to an object """
        tag = Tag({'@id': None})

        if hasattr(obj, 'get_resource_type'):
            entity = obj.get_resource_type()
        else:
            entity = obj.entity

        tag.resource = {
            '@id': obj.id,
            'type': entity
        }
        return tag
