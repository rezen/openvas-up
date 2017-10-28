import pytest
import openvasup.util as util

class Cat(object): pass

class TestUtil:

    def test_to_entity(self):
        assert util.to_entity(Cat) == 'cat'

    def test_to_entity_instance(self):
        assert util.to_entity(Cat()) == 'cat'

    def test_to_entity_grab_attr(self):
        Cat.entity = 'dog'
        assert util.to_entity(Cat) == 'dog'
