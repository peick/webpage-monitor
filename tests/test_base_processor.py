import flexmock
import pytest

from webpage_monitor.base_processor import BaseProcessor, set_shutdown_flag


def test_step_failed():
    proc = BaseProcessor()

    flexmock(proc).should_receive("step").and_raise(KeyError())
    flexmock(proc).should_receive("shutdown").once()

    with pytest.raises(KeyError):
        proc()


def test_step_signal():
    proc = BaseProcessor()

    flexmock(proc).should_receive("step").never()
    flexmock(proc).should_receive("shutdown").once()

    set_shutdown_flag(True)
    proc()
    set_shutdown_flag(False)
