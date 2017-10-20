""" User admin related models """
from model import OpenvasObject
import field

class Group(OpenvasObject):
    name = field.Text().required()
    comment = field.Text()
    users = field.TextCsv()

class Role(OpenvasObject):
    name = field.Text().required()
    comment = field.Text()

class User(OpenvasObject):
    name = field.Text().required()
    comment = field.Text()
    role = field.Object(Role)
    users = field.TextCsv()
