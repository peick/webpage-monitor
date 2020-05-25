import threading

import psycopg2
import pytest
from kafka import KafkaConsumer, KafkaProducer

from webpage_monitor.base_processor import set_shutdown_flag
from webpage_monitor.collector.processor import WebpageStatusProcessor
from webpage_monitor.pgwriter.processor import PgWriterProcessor


# module is marked as integration test. Requires kafka and postgres running.
pytestmark = [
    pytest.mark.integ,
    pytest.mark.usefixtures("collector", "pgwriter", "shutdown_on_exit"),
]

TOPIC = "webpage-checks"


def _create_collector(url, pytestconfig):
    """Creates a WebpageStatusProcessor connected to the kafka test instance.
    """
    max_messages_per_second = 100
    interval = 1. / max_messages_per_second
    bootstrap_server = pytestconfig.getoption("kafka_bootstrap_server")
    kafka_producer = KafkaProducer(bootstrap_servers=[bootstrap_server])
    processor = WebpageStatusProcessor(kafka_producer, TOPIC, interval, url, pattern=".*")

    return processor


def _create_pgwriter(pytestconfig):
    """Creates a PgWriterProcessor connected to the postgres test instance.
    """
    pg_connection = psycopg2.connect(
        dbname=pytestconfig.getoption("postgres_dbname"),
        user=pytestconfig.getoption("postgres_user"),
        password=pytestconfig.getoption("postgres_password"),
        host=pytestconfig.getoption("postgres_host"),
    )
    bootstrap_server = pytestconfig.getoption("kafka_bootstrap_server")
    kafka_consumer = KafkaConsumer(
        bootstrap_servers=[bootstrap_server], group_id="test"
    )
    processor = PgWriterProcessor(
        pg_connection, kafka_consumer, TOPIC, ["webpage_checks"]
    )

    return processor


@pytest.fixture
def collector(pytestconfig, httpserver):
    processor = _create_collector(httpserver.url, pytestconfig)

    thread = threading.Thread(target=processor)
    thread.daemon = True
    thread.start()

    try:
        yield thread
    finally:
        print "teardown collector"
        set_shutdown_flag(True)
        thread.join(60)


@pytest.fixture
def pgwriter(pytestconfig):
    processor = _create_pgwriter(pytestconfig)

    thread = threading.Thread(target=processor)
    thread.daemon = True
    thread.start()

    try:
        yield thread
    finally:
        print "teardown pgwriter"
        set_shutdown_flag(True)
        thread.join(60)


@pytest.fixture(scope="module")
def shutdown_on_exit():
    yield
    print "teardown all"
    set_shutdown_flag(True)


def test_all_components(httpserver):
    httpserver.serve_content('no body', 200)
    import time

    for i in range(30):
        print i
        time.sleep(1)
