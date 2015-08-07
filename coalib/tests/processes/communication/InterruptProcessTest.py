import multiprocessing
import platform
import sys
import time
import unittest

sys.path.insert(0, ".")
from coalib.processes.communication.InterruptProcess import interrupt_process
from coalib.processes.Processing import create_process_group


def runner(queue):
    try:
        while True:
            queue.put("Hello coala", timeout=0.1)
            time.sleep(0.9)
    finally:
        queue.put("End", timeout=0.1)


def runner2(queue):
    try:
        runner(queue)
    finally:
        queue.put("End2", timeout=0.1)


class InterruptProcessTest(unittest.TestCase):
    def test_interrupt_process(self):
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=runner, kwargs={'queue': queue})
        p.start()
        time.sleep(2)
        interrupt_process(p.pid)
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("End", queue.get(timeout=0.1))
        p.terminate()
        p.join()

    def test_interrupt_process_with_nested_functions(self):
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=runner2, kwargs={'queue': queue})
        p.start()
        time.sleep(2)
        interrupt_process(p.pid)
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("Hello coala", queue.get(timeout=0.1))
        self.assertEqual("End", queue.get(timeout=0.1))
        self.assertEqual("End2", queue.get(timeout=0.1))
        p.terminate()
        p.join()


if __name__ == '__main__':
    if platform.system() == "Windows":
        if len(sys.argv) > 1 and sys.argv[1] == "ActivateTestProcess":
            sys.argv = [sys.argv[0]] + sys.argv[2:]
            unittest.main(verbosity=2)
        else:
            proc = create_process_group((sys.executable,
                                         __file__,
                                         "ActivateTestProcess")
                                         + tuple(sys.argv[2:]))
            proc.wait()
    else:
        unittest.main(verbosity=2)
