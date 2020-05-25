import logging
from argparse import ArgumentParser


def get_argument_parser():
    parser = ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase log level",
    )
    parser.add_argument(
        "--kafka-host",
        help="Hostname of the kafka server. Default: %(default)s",
        default="localhost",
    )
    parser.add_argument(
        "--kafka-port",
        help="Port of the kafka server. Default: %(default)s",
        default=9092,
        type=int,
    )
    parser.add_argument(
        "--kafka-topic",
        required=True,
        help="The kafka topic to read from or publish to")

    return parser


def init_logging(verbose):
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)
