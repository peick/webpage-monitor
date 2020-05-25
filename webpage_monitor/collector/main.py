import logging
import os
import sys

from kafka import KafkaProducer

from webpage_monitor import cli_commons
from webpage_monitor.base_processor import register_signal_handler
from webpage_monitor.collector.processor import WebpageStatusProcessor


_log = logging.getLogger(__name__)


def _get_cli_args():
    parser = cli_commons.get_argument_parser()

    parser.add_argument("--url", required=True, help="The url to monitor")
    parser.add_argument(
        "--pattern", help="A regular expression checked on the downloaded webpage"
    )
    parser.add_argument(
        "--interval",
        type=int,
        help="Check interval in seconds. Default: %(default)s",
        default=5,
    )

    return parser.parse_args()


def _create_kafka_producer(args):
    server = "{}:{}".format(args.kafka_host, args.kafka_port)
    kafka_producer = KafkaProducer(bootstrap_servers=[server], retries=5)

    return kafka_producer


def main():
    args = _get_cli_args()
    cli_commons.init_logging(args.verbose)
    register_signal_handler()

    kafka_producer = _create_kafka_producer(args)
    processor = WebpageStatusProcessor(
        kafka_producer,
        args.kafka_topic,
        args.interval,
        args.url,
        pattern=args.pattern,
    )

    try:
        processor()
    except Exception:
        _log.error("error in processor", exc_info=True)
        sys.exit(os.EX_SOFTWARE)

    sys.exit(os.EX_OK)
