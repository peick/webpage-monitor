"""Reads webpage metrics from kafka topic and writes them to destination table(s).

If multiple tables are specified, then the partition of the kafka record is mapped
to an index of the tables with:

    tables[partition % len(tables)]

Ideally, the number of tables equals the number of partitions.
"""
import logging
import os
import sys

import psycopg2
from kafka import KafkaConsumer

from webpage_monitor import cli_commons
from webpage_monitor.base_processor import register_signal_handler
from webpage_monitor.pgwriter.processor import PgWriterProcessor


_log = logging.getLogger(__name__)


def _get_cli_args():
    parser = cli_commons.get_argument_parser()

    parser.add_argument(
        "--kafka-group-id",
        default="pgwriter",
        help="Kafka consumer group. Default: %(default)s",
    )
    parser.add_argument("--db-host", required=True, help="Postgress server hostname")
    parser.add_argument("--db-port", type=int, default=5432)
    parser.add_argument("--db-user", required=True, help="Database username")
    parser.add_argument("--db-password", required=True, help="Database password")
    parser.add_argument("--db-name", required=True, help="Database to use")
    parser.add_argument("--db-table", action="append", required=True)

    return parser.parse_args()


def _create_kafka_consumer(args):
    server = "{}:{}".format(args.kafka_host, args.kafka_port)
    kafka_consumer = KafkaConsumer(
        bootstrap_servers=[server], group_id=args.kafka_group_id,
    )

    return kafka_consumer


def _create_pg_connection(args):
    return psycopg2.connect(
        user=args.db_user,
        password=args.db_password,
        host=args.db_host,
        port=args.db_port,
        database=args.db_name,
    )


def main():
    args = _get_cli_args()
    cli_commons.init_logging(args.verbose)
    register_signal_handler()

    pg_connection = _create_pg_connection(args)
    kafka_consumer = _create_kafka_consumer(args)
    processor = PgWriterProcessor(
        pg_connection, kafka_consumer, args.kafka_topic, args.db_table
    )

    try:
        processor()
    except Exception:
        _log.error("error in processor", exc_info=True)
        sys.exit(os.EX_SOFTWARE)

    sys.exit(os.EX_OK)
