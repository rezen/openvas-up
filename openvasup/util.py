""" General purpose utils """
from __future__ import print_function
# @todo compat for python versions

def omp_filter_from_dict(data):
    return "".join(['%s="%s"' % (k, v) for k, v in data.items()])

def to_entity(obj):
    """ Get an entity name from the object """
    if hasattr(obj, 'entity'):
        return getattr(obj, 'entity')

    if isinstance(obj, type):
        return obj.__name__.lower()
    return obj.__class__.__name__.lower()

class ObservableDict(dict):
    """ Track changes for dict and nested dictionaries """
    def _onchange(self):
        if hasattr(self, '_callback'):
            self._callback()
        self.changed = True

    def __init__(self, *args, **kwargs):
        self.changed = False
        callback = kwargs.pop('callback') if 'callback' in kwargs else None
        if callable(callback):
            self._callback = callback

        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, item):
        if key in self and self[key] == item:
            return
        if isinstance(item, dict) and not isinstance(item, ObservableDict):
            item = ObservableDict(item, callback=self._onchange)
        dict.__setitem__(self, key, item)
        self._onchange()

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._onchange()

class ObservableList(list):

    def __new__(cls, *args, **kwargs):
        def _wrap_method(name, method):
            def inner(self, *a, **k):
                self._onchange()
                return method(self, *a, **k)
            return inner
        
        modifiers = [
            '__add__',  '__delattr__',
            '__delitem__', '__delslice__', 
            '__rmul__', '__setitem__',
            '__setslice__', 
            'append',   'extend',
            'insert', 'pop', 'remove', 'reverse', 'sort',
        ]

        for fn in modifiers:
            method = getattr(cls, fn)
            setattr(cls, fn, _wrap_method(fn, method))
        return super(ObservableList, cls).__new__(cls, *args, **kwargs)


    def __init__(self, *args, **kwargs):
        self.changed = False
        callback = kwargs.pop('callback') if 'callback' in kwargs else None
        if callable(callback):
            self._callback = callback

        return super(ObservableList, self).__init__(*args, **kwargs)

    def _onchange(self):
        if hasattr(self, '_callback'):
            self._callback()
        self.changed = True
    
