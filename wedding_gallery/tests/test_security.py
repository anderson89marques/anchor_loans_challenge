import unittest
from pyramid.testing import DummyRequest


class TestMyAuthenticationPolicy(unittest.TestCase):

    def test_no_user(self):
        request = DummyRequest()
        request.user = None

        from  wedding_gallery.security import MyAuthenticationPolicy
        policy = MyAuthenticationPolicy(None)
        self.assertEqual(policy.authenticated_userid(request), None)

    def test_authenticated_user(self):
        from wedding_gallery.models import User
        request = DummyRequest()
        request.user = User()
        request.user.id = 'foo'

        from  wedding_gallery.security import MyAuthenticationPolicy
        policy = MyAuthenticationPolicy(None)
        self.assertEqual(policy.authenticated_userid(request), 'foo')