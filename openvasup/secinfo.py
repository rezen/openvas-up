""" Models related to nvt, cve, etc """
from model import OpenvasObject
import field

class Nvt(OpenvasObject):
    """ Network vulnerability test """
    name = field.Text()
    category = field.Text()
    default_filter = {'@details':'1'}
