import sys
import json
import unittest
from datetime import datetime

sys.path.insert(0, ".")
from coalib.output.JSONEncoder import JSONEncoder


class TestClass1(object):
    def __init__(self):
        self.a = 0


class TestClass2(object):
    def __init__(self):
        self.a = 0
        self.b = TestClass1()


class TestClass3(object):
    def __init__(self):
        self.a = 0
        self.b = TestClass1()

    @staticmethod
    def __getitem__(key):
        return "val"

    @staticmethod
    def keys():
        return ["key"]


class JSONEncoderTest(unittest.TestCase):
    kw = {"cls": JSONEncoder, "sort_keys": True}

    def test_builtins(self):
        self.assertEquals('"test"', json.dumps("test", **self.kw))
        self.assertEquals('1', json.dumps(1, **self.kw))
        self.assertEquals('true', json.dumps(True, **self.kw))
        self.assertEquals('null', json.dumps(None, **self.kw))

    def test_iter(self):
        self.assertEquals('[0, 1]', json.dumps([0, 1], **self.kw))
        self.assertEquals('[0, 1]', json.dumps((0, 1), **self.kw))
        self.assertEquals('[0, 1]', json.dumps(range(2), **self.kw))

    def test_dict(self):
        self.assertEquals('{"0": 1}', json.dumps({0: 1}, **self.kw))
        self.assertEquals('{"0": 1}', json.dumps({"0": 1}, **self.kw))
        self.assertEquals('{"0": "1"}', json.dumps({"0": "1"}, **self.kw))

    def test_time(self):
        tf = datetime.today()
        self.assertEquals('"' + tf.isoformat() + '"',
                          json.dumps(tf, **self.kw))

    def test_class(self):
        tc1 = TestClass1()
        self.assertEquals('{"a": 0}', json.dumps(tc1, **self.kw))
        self.assertEquals('[{"a": 0}]', json.dumps([tc1], **self.kw))
        self.assertEquals('{"0": {"a": 0}}', json.dumps({0: tc1}, **self.kw))
        tc2 = TestClass2()
        self.assertEquals('{"a": 0, "b": {"a": 0}}',
                          json.dumps(tc2, **self.kw))
        tc3 = TestClass3()
        self.assertEquals('{"key": "val"}',
                          json.dumps(tc3, **self.kw))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            json.dumps(1j, **self.kw)


if __name__ == "__main__":
    unittest.main(verbosity=2)
