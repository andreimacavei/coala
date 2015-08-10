import sys
import unittest

sys.path.insert(0, ".")
from coalib.processes.communication.InterruptCoala import interrupt_coala


# TODO: This is an integration test. Just start and cancel coala. Maybe use
# and indeterminate bear for that so we have reliable cancelling.
class InterruptCoalaTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
