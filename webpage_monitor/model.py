import json

from schematics.models import Model
from schematics.types import BooleanType, IntType


class ErrorCodes(object):
    NO_ERROR = 0
    CONNECTION_ERROR = 1
    TIMEOUT = 2
    UNKNOWN_ERROR = 3


class WebpageMetric(Model):
    # timestamp
    http_response_time = IntType(required=True)

    http_status_code = IntType()

    # when server did not respond, error_code is set
    error_code = IntType()

    pattern_found = BooleanType()


def to_json(model):
    data = model.to_primitive()
    return json.dumps(data)


def from_json(serialized_json):
    try:
        data = json.loads(serialized_json)
    except (ValueError, TypeError):
        raise ValueError("no json data found")

    try:
        metric = WebpageMetric(data)
        metric.validate()
    except Exception as error:
        raise ValueError("invalid metric: {}".format(error))

    return metric
