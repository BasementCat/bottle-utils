import json

import unittest
import bottle
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound

from bottleutils.database import SQLAlchemyNotFoundPlugin, SQLAlchemySession

class MockSession(object):
    def __init__(self):
        self.commit_calls = 0
        self.close_calls = 0

    def commit(self):
        self.commit_calls += 1

    def close(self):
        self.close_calls += 1

class MockSessionMaker(object):
    def __init__(self, bind = None):
        self.bind = bind

    def __call__(*args, **kwargs):
        return MockSession()

class MockEngine(object):
    pass

class TestSQLAlchemyNotFoundPlugin(unittest.TestCase):
    def test_plugin(self):
        plugin = SQLAlchemyNotFoundPlugin()

        def test_plugin_fn(do_raise):
            if do_raise:
                raise NoResultFound()

        test_fn = plugin.apply(test_plugin_fn, None)

        test_fn(False)

        try:
            test_fn(True)
            self.assertTrue(False, "No exception was raised")
        except bottle.HTTPError as e:
            self.assertEquals(404, e.status_code)
            self.assertEquals("Item not found", e.body)

class TestSQLAlchemySession(unittest.TestCase):
    def setUp(self):
        self.old_maker = sqlalchemy.orm.sessionmaker
        sqlalchemy.orm.sessionmaker = MockSessionMaker

    def tearDown(self):
        sqlalchemy.orm.sessionmaker = self.old_maker

    def test_plugin(self):
        engine = MockEngine()
        plugin = SQLAlchemySession(engine)
        self.assertIs(plugin.engine, engine)
        self.assertIsInstance(plugin.maker, MockSessionMaker)

        def test_plugin_fn():
            pass

        test_fn = plugin.apply(test_plugin_fn, None)
        test_fn()

        self.assertEquals(0, bottle.request.sa_session.commit_calls)
        self.assertEquals(1, bottle.request.sa_session.close_calls)
