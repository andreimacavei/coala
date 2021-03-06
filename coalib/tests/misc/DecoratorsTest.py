import unittest
import sys

sys.path.insert(0, ".")
from coalib.misc.Decorators import (arguments_to_lists,
                                    yield_once,
                                    generate_repr)


class YieldOnceTest(unittest.TestCase):
    def test_yield_once(self):
        @yield_once
        def iterate_over_list(arg_list):
            for arg in arg_list:
                yield arg

        self.assertEqual(list(iterate_over_list([1, 1, 2, 2, 3, 3, 1, 4])),
                         [1, 2, 3, 4])


class ArgumentsToListsTest(unittest.TestCase):
    def test_arguments_to_lists(self):
        @arguments_to_lists
        def return_args(*args, **kwargs):
            return args, kwargs

        self.assertEqual(
            return_args(None, True, 1, "", "AB", [1, 2], t=(3, 4), d={"a": 1}),
            (([], [True], [1], [""], ["AB"], [1, 2]), {"t": [3, 4],
                                                       "d": [{"a": 1}]
                                                       })
        )


class GenerateReprTest(unittest.TestCase):
    # We can't define the class in the scope of this test because generate_repr
    # modifies the class in place, so we need to redefine it every time.
    @staticmethod
    def define_class():
        class X:
            def __init__(self):
                self.A = 2
                self.B = "A string"
                self.ComplexMember = [3, 2, 1]
                self.Q = 0.5
                self.one = 1
                self._private_member = 0
                self.__DONT_TOUCH = 1

            def computeA(self):
                return self.A ** 3 - 7

            @property
            def getter(self):
                return self.one * "getter()"

            @property
            def _private_prop(self):
                return self.one

            @property
            def defaulted_getter(self, a=3, b=2):
                return a * b * self.one

            def getter_like_function(self):
                return ["A", "B"] * self.one

            def defaulted_getter_like_function(self, num=33):
                return (num, num + self.one, num + self.one * 2)

            def polynome(self, x, a, b, c):
                return a + b * x + self.one * c * x ** 2

        return X

    def test_manual_argument_list(self):
        X = generate_repr("A")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=2\\) at 0x[0-9a-fA-F]+>")

        X = generate_repr("A", "B")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=2, B='A string'\\) at 0x[0-9a-fA-F]+>")

        X = generate_repr("A", "B", "ComplexMember")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=2, B='A string', ComplexMember=\\[3, "
                             "2, 1\\]\\) at 0x[0-9a-fA-F]+>")

        X = generate_repr("A", "B", "ComplexMember", "Q")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=2, B='A string', "
                             "ComplexMember=\\[3, 2, 1\\]\\, Q=0\\.5\\) at "
                             "0x[0-9a-fA-F]+>")

        # Switch order.
        X = generate_repr("ComplexMember", "A")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(ComplexMember=\\[3, 2, 1\\], A=2\\) at "
                             "0x[0-9a-fA-F]+>")

        X = generate_repr("Q", "ComplexMember", "A", "B")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(Q=0\\.5, ComplexMember=\\[3, 2, 1\\], "
                             "A=2, B='A string'\\) at 0x[0-9a-fA-F]+>")

    def test_manual_argument_list_with_custom_repr(self):
        X = generate_repr(("A", lambda x: str(x ** 2)))(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=4\\) at 0x[0-9a-fA-F]+>")

        X = generate_repr(("A", lambda x: str(x ** 2)), ("B", None))
        X = X(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=4, B='A string'\\) at 0x[0-9a-fA-F]+>")

        X = generate_repr(
            ("B", None),
            ("A", lambda x: str(x ** 2)),
            ("ComplexMember", lambda x: ".".join(str(v) for v in x)))
        X = X(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(B='A string', A=4, "
                             "ComplexMember=3\\.2\\.1\\) at 0x[0-9a-fA-F]+>")

        # Combine normal strings with tuples.
        X = generate_repr("A",
                          ("B", str),
                          "ComplexMember",
                          ("Q", lambda x: "OVERRIDE"))
        X = X(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=2, B=A string, "
                             "ComplexMember=\\[3, 2, 1\\], Q=OVERRIDE\\) at "
                             "0x[0-9a-fA-F]+>")

    def test_properties(self):
        X = generate_repr("getter")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(getter='getter\\(\\)'\\) at "
                             "0x[0-9a-fA-F]+>")

        X = generate_repr("A",
                          "getter",
                          "defaulted_getter")
        X = X(self.define_class())

        self.assertRegex(repr(X()),
                         "<X object\\(A=2, getter='getter\\(\\)', "
                             "defaulted_getter=6\\) at 0x[0-9a-fA-F]+>")

    def test_getter_like_functions(self):
        X = generate_repr("getter_like_function")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(getter_like_function=\\['A', 'B'\\]\\) "
                             "at 0x[0-9a-fA-F]+>")

        X = generate_repr("defaulted_getter_like_function")
        X = X(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(defaulted_getter_like_function=\\(33, "
                             "34, 35\\)\\) at 0x[0-9a-fA-F]+>")

    def test_invalid_attribute(self):
        X = generate_repr("A", "B", "INVALID")(self.define_class())
        self.assertRaises(AttributeError, repr, X())

        X = generate_repr("A", "polynome")(self.define_class())
        self.assertRaises(TypeError, repr, X())

    def test_invalid_argument_tuple_size(self):
        self.assertRaises(ValueError, generate_repr, (88,))
        self.assertRaises(ValueError, generate_repr, ("A", repr, 3, 4))
        self.assertRaises(ValueError, generate_repr, ("A", repr, False))
        self.assertRaises(ValueError,
                          generate_repr,
                          ("A", repr),
                          ("B", None),
                          ("Q", 3, 2, 1, 0))

    def test_auto_repr(self):
        X = generate_repr()(self.define_class())
        x = X()

        self.assertRegex(repr(x),
                         "<X object\\(A=2, B='A string', ComplexMember=\\[3, "
                         "2, 1\\], defaulted_getter=6, getter='getter\\(\\)', "
                         "one=1, Q=0\\.5\\) at 0x[0-9a-fA-F]+>")

        # Insert member after instantation.
        x.Z = 17
        self.assertRegex(repr(x),
                         "<X object\\(A=2, B='A string', ComplexMember=\\[3, "
                         "2, 1\\], defaulted_getter=6, getter='getter\\(\\)', "
                         "one=1, Q=0\\.5, Z=17\\) at 0x[0-9a-fA-F]+>")

        # Test alphabetical order a bit more.
        x.Ba = 4
        x.g_mem = 0
        self.assertRegex(repr(x),
                         "<X object\\(A=2, B='A string', Ba=4, "
                         "ComplexMember=\\[3, 2, 1\\], defaulted_getter=6, "
                         "g_mem=0, getter='getter\\(\\)', one=1, Q=0\\.5, "
                         "Z=17\\) at 0x[0-9a-fA-F]+>")

    def test_duplicate_member(self):
        X = generate_repr("A", "A")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=2, A=2\\) at 0x[0-9a-fA-F]+>")

        X = generate_repr("A", "B", "A")(self.define_class())
        self.assertRegex(repr(X()),
                         "<X object\\(A=2, B='A string', A=2\\) at "
                             "0x[0-9a-fA-F]+>")

if __name__ == '__main__':
    unittest.main(verbosity=2)
