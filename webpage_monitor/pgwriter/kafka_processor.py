import logging

import six
from kafka import OffsetAndMetadata

from webpage_monitor.base_processor import BaseProcessor


_log = logging.getLogger(__name__)


class KafkaConsumerProcessor(BaseProcessor):
    """Polls a batch of records from kafka, processes them and commits the consumer
    offset. The offset is committed _after_ the call to `_commit` to make sure no
    record is lost.

    This, whatever happens in `_commit` must be prepared to work on the same records
    twice, because of the at-least-once semantics in kafka.
    """

    def __init__(self, kafka_consumer, topic, poll_timeout_ms=10000):
        self._consumer = kafka_consumer
        self._poll_timeout_ms = poll_timeout_ms

        self._consumer.subscribe(topic)

        # we commit by hand
        self._consumer.config["enable_auto_commit"] = False

        # TopicPartition -> offset
        self._consumer_offsets = {}

    def step(self):
        """Fetches a batch of kafka records and processes them. Commits the offset(s)
        at the end.
        """
        # kafka consumer group offset commit. `.poll` does not return all fetched records.
        # Thus we commit only the consumed offsets per partition using _commit_offsets
        record_map = self._consumer.poll(timeout_ms=self._poll_timeout_ms)
        for tp, records in six.iteritems(record_map):
            for record in records:
                self._consumer_offsets[tp] = record.offset
                self._handle_message(record)

        self._commit()

        if self._consumer_offsets:
            _log.warn("there are uncommitted offsets for some partitions")

    def shutdown(self):
        self._consumer.close()

    def _commit_offsets(self, partition):
        """Commit kafka consumer group offsets.
        """
        commit_offsets = {}
        to_delete = []
        for tp, offset in six.iteritems(self._consumer_offsets):
            if tp.partition == partition:
                commit_offsets[tp] = OffsetAndMetadata(offset, None)
                to_delete.append(tp)

        for tp in to_delete:
            del self._consumer_offsets[tp]

        self._consumer.commit(commit_offsets)

    def _handle_message(self, message):
        """To be implemented in the sub-class.
        """
        raise NotImplementedError()

    def _commit(self):
        """To be implemented in the sub-class.

        The sub-class is responsible to call _commit_offsets once per partition of
        records seen in _handle_message.
        """
        raise NotImplementedError()
