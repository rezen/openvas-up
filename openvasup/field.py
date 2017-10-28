""" Fields for creating openvas object schemeas """
from xml.etree.ElementTree import Element
from xml.etree import ElementTree 

class FieldDescriptor(object):

    def __init__(self, field):
        self.field = field
        self.attr = self.field.name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            return instance._data.get(self.attr)
        return self.field

    def __set__(self, instance, value):
        if self.field.readonly is True:
            pass

        if self.field.dtype is not None and value is not None:
            if not isinstance(value, self.field.dtype):
                if isinstance(value, Element) and hasattr(self.field.dtype, 'from_xml'):
                    value = self.field.dtype.from_xml(value)
                else:
                    try:
                        value = self.field.dtype(value)
                    except:
                        print('FAILED %s %s' % (self.field.dtype, type(value)))

        if instance._data.get(self.attr) == value:
            return

        instance._prev[self.attr] = instance.get_attr(self.attr)
        instance._data[self.attr] = value
        instance._dirty.add(self.attr)

class Field(object):

    def add_to_class(self, cls, name):
        """ Adds field descriptor to OpenvasObject classes """
        cls.fields.append(self)
        cls.field_names.append(name)

        if self.is_required is True:
            cls.required.append(name)

        self.model = cls
        self.name = name
        self.cls = cls

        # print('add_to_class %s %s' % (name, cls))
        setattr(cls, name, FieldDescriptor(self))
        self._is_bound = True


    def __init__(self, model=None, **kwargs):
        self.dtype = model
        self.editable = kwargs.get('editable', True)
        self.is_required = kwargs.get('is_required', False)
        self.model = None
        self.readonly = kwargs.get('readonly', False)


    def required(self):
        """ Set the field to required """
        self.is_required = True
        return self

class Text(Field): pass

class Object(Field): pass

class Uuid(Field): pass

class TextCsv(Field): pass

class Integer(Field): pass

class Boolean(Field): pass

class Base64(Field): pass