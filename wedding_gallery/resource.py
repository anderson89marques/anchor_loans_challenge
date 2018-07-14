"""Define the ACL"""
from pyramid.security import Allow, Everyone, ALL_PERMISSIONS, Authenticated

acl_registered_permission = [(Allow, 'role:basic', 'registered'), (Allow, 'role:admin', 'registered'),]
acl_admin_permission = [(Allow, 'role:admin', 'admin')]

class RootResource:
    def __init__(self, request):
        pass

    def __acl__(self):
        return acl_registered_permission + acl_admin_permission
