import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.Result import Result, RESULT_SEVERITY


class ResultTest(unittest.TestCase):
    def test_wrong_types(self):
        uut = Result('b', 'b')
        self.assertNotEqual(uut, 0)
        self.assertRaises(TypeError, uut.__ge__, 0)
        self.assertRaises(TypeError, uut.__le__, 0)
        self.assertRaises(TypeError, uut.__gt__, 0)
        self.assertRaises(TypeError, uut.__lt__, 0)

    def test_origin(self):
        uut = Result("origin", "msg")
        self.assertEqual(uut.origin, "origin")

        uut = Result(self, "msg")
        self.assertEqual(uut.origin, "ResultTest")

        uut = Result(None, "msg")
        self.assertEqual(uut.origin, "")

    def test_string_conversion(self):
        uut = Result('a', 'b', 'c')
        self.assertEqual(str(uut),
                         "Result:\n origin: 'a'\n file: 'c'\n line nr: None\n"
                         " severity: 1\n'b'")
        self.assertRegex(
            repr(uut),
            "<Result object\\(origin='a', file='c', line_nr=None, "
                "severity=NORMAL, message='b'\\) at 0x[0-9a-fA-F]+>")
        self.assertEqual(
            Result("origin", "message", "file", line_nr=1).__str__(),
            """Result:
 origin: 'origin'
 file: 'file'
 line nr: 1
 severity: 1
'message'""")

    def test_ordering(self):
        """
        Tests the ordering routines of Result. This tests enough to have all
        branches covered. Not every case may be covered but I want to see the
        (wo)man who writes comparison routines that match these criteria and
        are wrong to the specification. (Given he does not engineer the routine
        to trick the test explicitly.)
        """
        medium = Result(origin='b',
                        message='b',
                        file='b',
                        severity=RESULT_SEVERITY.NORMAL)
        medium_too = Result(origin='b',
                            message='b',
                            file='b',
                            severity=RESULT_SEVERITY.NORMAL)
        self.assert_equal(medium, medium_too)

        bigger_file = Result(origin='b',
                             message='b',
                             file='c',
                             severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(bigger_file, medium)

        no_file = Result(origin='b',
                         message='b',
                         file=None,
                         severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(medium, no_file)

        no_file_and_unsevere = Result(origin='b',
                                      message='b',
                                      file=None,
                                      severity=RESULT_SEVERITY.INFO)
        self.assert_ordering(no_file_and_unsevere, no_file)
        self.assert_ordering(medium, no_file_and_unsevere)

        greater_origin = Result(origin='c',
                                message='b',
                                file='b',
                                severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(greater_origin, medium)

        medium.line_nr = 5
        greater_origin.line_nr = 3
        self.assert_ordering(medium, greater_origin)

        uut = Result("origin", "message", "file", line_nr=1)
        cmp = Result("origin", "message", "file", line_nr=1)
        self.assert_equal(cmp, uut)
        cmp = Result("origin", "message", "file")
        self.assertNotEqual(cmp, uut)

        cmp = Result("origin", "", "file", line_nr=1, debug_msg="test")
        self.assert_ordering(uut, cmp)

        cmp = Result("origin", "message", "file", line_nr=1, debug_msg="test")
        self.assertNotEqual(cmp, uut)
        self.assert_ordering(cmp, uut)

    def assert_equal(self, first, second):
        self.assertGreaterEqual(first, second)
        self.assertEqual(first, second)
        self.assertLessEqual(first, second)

    def assert_ordering(self, greater, lesser):
        self.assertGreater(greater, lesser)
        self.assertGreaterEqual(greater, lesser)
        self.assertNotEqual(greater, lesser)
        self.assertLessEqual(lesser, greater)
        self.assertLess(lesser, greater)

    def test_string_dict(self):
        uut = Result(None, None)
        output = uut.to_string_dict()
        self.assertEqual(output, {"origin": "",
                                  "message": "",
                                  "file": "",
                                  "line_nr": "",
                                  "severity": "NORMAL",
                                  "debug_msg": ""})

        uut = Result(origin="origin",
                     message="msg",
                     file="file",
                     line_nr=2,
                     severity=RESULT_SEVERITY.INFO,
                     debug_msg="dbg")
        output = uut.to_string_dict()
        self.assertEqual(output, {"origin": "origin",
                                  "message": "msg",
                                  "file": "file",
                                  "line_nr": "2",
                                  "severity": "INFO",
                                  "debug_msg": "dbg"})


        uut = Result(origin="origin", message="msg", line_nr="a")
        output = uut.to_string_dict()
        self.assertEqual(output["line_nr"], "a")


if __name__ == '__main__':
    unittest.main(verbosity=2)
