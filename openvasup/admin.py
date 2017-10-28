""" User admin related models """
from model import OpenvasObject
import field

class Group(OpenvasObject):
    """ A user can belong to many groups """
    name = field.Text().required()
    comment = field.Text()
    users = field.TextCsv()

class Role(OpenvasObject):
    """
    A user has a role which gives them permissions
    such as Admin, Super Admin, Monitor, etc
    """
    name = field.Text().required()
    comment = field.Text()

class User(OpenvasObject):
    """ A user is can do things ... """
    name = field.Text().required()
    comment = field.Text()
    role = field.Object(Role)
    users = field.TextCsv()
