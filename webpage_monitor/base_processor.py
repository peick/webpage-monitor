import logging
import signal


_log = logging.getLogger(__name__)

_shutdown_requested = False


def set_shutdown_flag(value):
    global _shutdown_requested
    _shutdown_requested = value


def _signal_shutdown(signum, frame):
    """Called when a SIGTERM / SIGINT is send to the process as a signal to shutdown
    the process.
    """
    _log.info("got a signal. Doing a graceful shutdown.")
    set_shutdown_flag(True)


def register_signal_handler():
    signal.signal(signal.SIGTERM, _signal_shutdown)
    signal.signal(signal.SIGINT, _signal_shutdown)


class BaseProcessor(object):
    def __call__(self):
        try:
            while not _shutdown_requested:
                self.step()
        finally:
            self.shutdown()

    def step(self):
        """To be implemented in sub-class.
        """
        raise NotImplementedError()

    def shutdown(self):
        """To be implemented in sub-class.
        """
        raise NotImplementedError()
