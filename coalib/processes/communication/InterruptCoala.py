import os
import platform
import signal


if platform.system() == "Windows":  # pragma: no cover
    _INTERRUPT_SIGNAL = signal.CTRL_C_EVENT
else:
    _INTERRUPT_SIGNAL = signal.SIGINT


def interrupt_coala(pid):
    """
    Interrupts a running coala process from outside.

    :param pid: The pid of coala.
    """
    os.kill(pid, _INTERRUPT_SIGNAL)
