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
