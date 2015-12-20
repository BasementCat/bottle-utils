import json
import datetime

import unittest
import bottle
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
import sqlalchemy_utils
import arrow

from bottleutils.database import SQLAlchemyNotFoundPlugin, SQLAlchemySession, SQLAlchemyJsonMixin

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

class TestSQLAlchemyJsonMixin(unittest.TestCase):
    def setUp(self):
        class Tester(SQLAlchemyJsonMixin, sqlalchemy.ext.declarative.declarative_base()):
            __tablename__ = 'tester'
            intField = sqlalchemy.Column(sqlalchemy.BigInteger(), primary_key=True)
            strField = sqlalchemy.Column(sqlalchemy.UnicodeText())
            noneField = sqlalchemy.Column(sqlalchemy.Integer())
            floatField = sqlalchemy.Column(sqlalchemy.Float())
            boolField = sqlalchemy.Column(sqlalchemy.Boolean())
            dateTimeField = sqlalchemy.Column(sqlalchemy.DateTime())
            arrowField = sqlalchemy.Column(sqlalchemy_utils.ArrowType())

        self.model = Tester
        self.now_dt = datetime.datetime.utcnow()
        self.now_arrow = arrow.utcnow()
        self.instance = self.model(
            intField=10,
            strField='hello world',
            noneField=None,
            floatField=7.2,
            boolField=True,
            dateTimeField=self.now_dt,
            arrowField=self.now_arrow,
        )

    def test_json(self):
        res = json.loads(json.dumps(self.instance.to_json()))
        self.assertEquals(10, res['intField'])
        self.assertEquals('hello world', res['strField'])
        self.assertEquals(None, res['noneField'])
        self.assertEquals(7.2, res['floatField'])
        self.assertEquals(True, res['boolField'])
        self.assertEquals(str(self.now_dt), res['dateTimeField'])
        self.assertEquals(str(self.now_arrow), res['arrowField'])