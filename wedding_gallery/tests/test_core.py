import unittest

import transaction
import webtest
from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:',
            'secret': 'seekrit',
            'auth.secret': 'authseekrit',
        })
        self.config.include('wedding_gallery.models')
        settings = self.config.get_settings()

        from wedding_gallery.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from wedding_gallery.models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from wedding_gallery.models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestPhotoSave(BaseTest):

    def setUp(self):
        super(TestPhotoSave, self).setUp()
        self.init_database()

        from wedding_gallery.models import Photo, User
        from uuid import uuid4

        user = User(name='husband', role='admin')
        user.set_password('admin')
        self.session.add(user)

        photo = Photo(name='anderson.jpg',
                      uuid=str(uuid4()),
                      description="my photo",
                      total_likes=0)
        photo.creator = user                      
        self.session.add(photo)

    def test_save_photo(self):
        from wedding_gallery.models import Photo
        self.assertTrue(self.session.query(Photo).count())


class PhotoViewTest(BaseTest):
    def setUp(self):
        super(PhotoViewTest, self).setUp()
        self.init_database()

        from wedding_gallery.models import Photo, User
        from uuid import uuid4

        user = User(name='husband', role='admin')
        user.set_password('admin')
        self.session.add(user)

        photo = Photo(name='anderson.jpg',
                      uuid=str(uuid4()),
                      description="my photo",
                      total_likes=0)
        photo.creator = user                      
        self.session.add(photo)

    def test_check_file_format_ok(self):
        from wedding_gallery.views.photo_views import PhotoView
        request = testing.DummyRequest(dbsession=self.session)
        inst = PhotoView(request)
        resp = inst.check_file_format("anderson.jpg")
        self.assertTrue(resp)

    def test_check_file_format_invalid(self):
        from wedding_gallery.views.photo_views import PhotoView
        request = testing.DummyRequest(dbsession=self.session)
        inst = PhotoView(request)
        resp = inst.check_file_format("anderson")
        self.assertFalse(resp)
    
    def test_show_photos(self):
        from wedding_gallery.views.photo_views import PhotoView
        request = testing.DummyRequest(dbsession=self.session)
        request.matchdict["page"] = 1
        inst = PhotoView(request)
        resp = inst.photos()
        self.assertTrue('photos' in resp)
        self.assertFalse(resp.get('photos'))
    
    def test_show_photos_tobe_approved(self):
        from wedding_gallery.views.photo_views import PhotoView
        request = testing.DummyRequest(dbsession=self.session)
        request.matchdict["page"] = 1
        inst = PhotoView(request)
        resp = inst.photos_tobe_approved()
        self.assertTrue('photos' in resp)
        self.assertTrue(resp.get('photos'))
    
    def test_approve_photo(self):
        from wedding_gallery.views.photo_views import PhotoView

        request = testing.DummyRequest(post={'photo_id': 1},
                                       dbsession=self.session)
        inst = PhotoView(request)
        resp = inst.approve_photo()
        self.assertEqual(resp.location, '/approve_photos')


class TestUserSave(BaseTest):

    def setUp(self):
        super(TestUserSave, self).setUp()
        self.init_database()

        from wedding_gallery.models import User

        user = User(name='husband', role='admin')
        user.set_password('admin')
        self.session.add(user)

    def makeUser(self, name, role):
        from wedding_gallery.models import User
        return User(name=name, role=role)

    def test_save_user(self):
        from wedding_gallery.models import User
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


class AuthFunctionalViewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from wedding_gallery.models.meta import Base
        from wedding_gallery.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            User
        )
        from wedding_gallery import main

        settings = {
            'sqlalchemy.url': 'sqlite:///:memory:',
            'secret': 'seekrit',
            'auth.secret': 'authseekrit',
        }

        app = main({}, **settings)
        cls.testapp = webtest.TestApp(app)

        session_factory = app.registry['dbsession_factory']
        cls.engine = session_factory.kw['bind']
        Base.metadata.create_all(bind=cls.engine)
        cls.dbsession = get_tm_session(session_factory, transaction.manager)

        with transaction.manager:
            dbsession = get_tm_session(session_factory, transaction.manager)
            from wedding_gallery.models import User
            user = User(name='usuario', role='basic')
            user.set_password('basic')
            dbsession.add(user)

    @classmethod
    def tearDownClass(cls):
        from wedding_gallery.models.meta import Base
        Base.metadata.drop_all(bind=cls.engine)

    def test_login_page(self):
        resp = self.testapp.get('/login', status=200)
        self.assertIn(b'Login', resp.body)

    def test_successful_login(self):
        resp = self.testapp.post('/login', params={'login': 'usuario', 'password': 'basic'},
                                 status=302)
        self.assertEqual(resp.location, 'http://localhost/')

    def test_failed_login(self):
        resp = self.testapp.post('/login', params={'login': 'usuario', 'password': 'incorrect'},
                                 status=200)
        self.assertEqual(resp.location, None)