import logging
from collections import defaultdict

from webpage_monitor import model
from webpage_monitor.pgwriter import db
from webpage_monitor.pgwriter.kafka_processor import KafkaConsumerProcessor


_log = logging.getLogger(__name__)


class PgWriterProcessor(KafkaConsumerProcessor):
    def __init__(self, pg_connection, kafka_consumer, topic, tables, **kwargs):
        super(PgWriterProcessor, self).__init__(kafka_consumer, topic, **kwargs)
        self._pg_connection = pg_connection
        self._metrics = defaultdict(list)
        self._tables = tables

    def _handle_message(self, record):
        try:
            metric = model.from_json(record.value)
        except ValueError as error:
            _log.warn("ignoring invalid record: %s", error)
            return

        self._metrics[record.partition].append(metric)

    def _commit(self):
        for partition, metrics in self._metrics.iteritems():
            table = self._tables[partition % len(self._tables)]
            db.insert_webpage_metrics(self._pg_connection, metrics, table)
            self._pg_connection.commit()
            self._commit_offsets(partition)
            _log.info(
                "wrote %d metrics of partition %d to table %s",
                len(metrics),
                partition,
                table,
            )

        self._metrics.clear()

    def shutdown(self):
        super(PgWriterProcessor, self).shutdown()
        self._pg_connection.close()
