import time

from webpage_monitor import model
from webpage_monitor.base_processor import BaseProcessor
from webpage_monitor.collector import check


class WebpageStatusProcessor(BaseProcessor):
    def __init__(self, kafka_producer, topic, interval, url, pattern=None):
        self._kafka_producer = kafka_producer
        self._topic = topic
        self._url = url
        self._pattern = pattern
        self._interval = interval

    def step(self):
        metric = check.check(self._url, pattern=self._pattern)
        data = model.to_json(metric)

        self._kafka_producer.send(self._topic, data)

        # flush immediately, no need to fill the send buffer
        self._kafka_producer.flush(timeout=5)

        time.sleep(self._interval)

    def shutdown(self):
        self._kafka_producer.close()
