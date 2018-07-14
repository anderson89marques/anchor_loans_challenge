import unittest

import transaction
from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestPhotoSave(BaseTest):

    def setUp(self):
        super(TestPhotoSave, self).setUp()
        self.init_database()

        from .models import Photo
        from uuid import uuid4

        photo = Photo(name='anderson.jpg',
                      uuid=str(uuid4()),
                      description="my photo",
                      likes=0)
        self.session.add(photo)

    def test_save_photo(self):
        from .models import Photo
        self.assertTrue(self.session.query(Photo).count())


class PhotoViewTest(unittest.TestCase):
    def test_check_file_format_ok(self):
        from wedding_gallery.views.photo_views import PhotoView
        request = testing.DummyRequest()
        inst = PhotoView(request)
        resp = inst.check_file_format("anderson.jpg")
        self.assertTrue(resp)

    def test_check_file_format_invalid(self):
        from wedding_gallery.views.photo_views import PhotoView
        request = testing.DummyRequest()
        inst = PhotoView(request)
        resp = inst.check_file_format("anderson")
        self.assertFalse(resp)


class TestUserSave(BaseTest):

    def setUp(self):
        super(TestUserSave, self).setUp()
        self.init_database()

        from .models import User

        user = User(name='husband', role='admin')
        user.set_password('admin')
        self.session.add(user)

    def makeUser(self, name, role):
        from .models import User
        return User(name=name, role=role)

    def test_save_user(self):
        from .models import User
        self.assertTrue(self.session.query(User).count())

    def test_password_hash_not_set(self):
        user = self.makeUser(name='foo', role='bar')
        self.assertFalse(user.check_password('secret'))

    def test_correct_password(self):
        user = self.makeUser(name='foo', role='bar')
        user.set_password('secret')
        self.assertTrue(user.password_hash)

    def test_incorrect_password(self):
        user = self.makeUser(name='foo', role='bar')
        user.set_password('secret')
        self.assertFalse(user.check_password('incorrect'))


class UserViewTest(BaseTest):
    def setUp(self):
        super(UserViewTest, self).setUp()
        self.init_database()

    def test_register_ok(self):
        from wedding_gallery.views.user_views import UserView

        request = testing.DummyRequest(post={'name': 'foo',
                                             'password': 'secret',
                                             'confirm': 'secret'},
                                       dbsession=self.session)
        inst = UserView(request)                                       
        response = inst.register()
        self.assertEqual(response.location, '/')

    def test_register_is_incorrect(self):
        from wedding_gallery.views.user_views import UserView

        request = testing.DummyRequest(post={'name': 'bar',
                                             'password': 'secret',
                                             'confirm': 'incorrect'},
                                       dbsession=self.session)
        inst = UserView(request)
        response = inst.register()
        self.assertEqual(response.location, '/register')
