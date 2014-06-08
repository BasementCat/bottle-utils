import json

import unittest
import bottle

from bottleutils.response import JsonResponsePlugin

class TestJsonResponsePlugin(unittest.TestCase):
    def test_formed_response(self):
        plugin = JsonResponsePlugin()

        def test_formed_response_fn(key):
            return {key: "foobar"}

        test_fn = plugin.apply(test_formed_response_fn, None)

        self.assertEquals({"result": "foobar"}, test_fn("result"))
        self.assertEquals({"error": "foobar"}, test_fn("error"))

    def test_unformed_response(self):
        plugin = JsonResponsePlugin()

        def test_unformed_response_fn():
            return {"foo": "bar"}

        test_fn = plugin.apply(test_unformed_response_fn, None)

        self.assertEquals({"result": {"foo": "bar"}}, test_fn())

    def test_error(self):
        plugin = JsonResponsePlugin()

        def test_error_fn():
            bottle.abort(500, "Internal error")
            return {"foo": "bar"}

        test_fn = plugin.apply(test_error_fn, None)

        try:
            test_fn()
        except bottle.HTTPResponse as e:
            self.assertEquals({"error": {"code": 500, "message": "Internal error"}}, json.loads(e.body))
