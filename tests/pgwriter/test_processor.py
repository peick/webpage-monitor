import flexmock
import pytest

from webpage_monitor.pgwriter import db
from webpage_monitor.pgwriter.processor import PgWriterProcessor


@pytest.fixture
def pg_mock():
    return flexmock()


@pytest.fixture
def consumer_mock():
    return flexmock(config={})


@pytest.fixture
def processor(consumer_mock, pg_mock):
    consumer_mock.should_receive("subscribe").once()
    inst = PgWriterProcessor(
        pg_mock, consumer_mock, "sample-topic", ["table0", "table1"]
    )

    return inst


def test_process_multiple(pg_mock, processor):
    flexmock(db).should_receive("insert_webpage_metrics").with_args(
        pg_mock, list, "table0"
    ).twice()
    flexmock(db).should_receive("insert_webpage_metrics").with_args(
        pg_mock, list, "table1"
    ).once()
    flexmock(pg_mock).should_receive("commit").times(3)
    flexmock(processor).should_receive("_commit_offsets").with_args(0).once()
    flexmock(processor).should_receive("_commit_offsets").with_args(1).once()
    flexmock(processor).should_receive("_commit_offsets").with_args(2).once()

    records = [
        flexmock(
            value='{"http_response_time": 1, "http_status_code": 200}', partition=0
        ),
        flexmock(
            value='{"http_response_time": 2, "http_status_code": 200}', partition=1
        ),
        flexmock(
            value='{"http_response_time": 3, "http_status_code": 200}', partition=2
        ),
    ]
    for record in records:
        processor._handle_message(record)

    processor._commit()

    assert len(processor._metrics) == 0
