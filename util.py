""" General purpose utils """
from __future__ import print_function
# @todo compat for python versions

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
        callback = kwargs.pop('callback')
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
