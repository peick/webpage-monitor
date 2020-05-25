import logging
import re
import time

import requests

from webpage_monitor.model import ErrorCodes, WebpageMetric


_log = logging.getLogger(__name__)


def check(url, pattern=None, timeout=1):
    """Connects to a url, fetches the content and tries to match the pattern if any.

    Any kind of error is tracked in the resulting metric object.

    Returns a WebpageMetric.
    """
    metric = WebpageMetric()

    try:
        response = requests.get(url, timeout=timeout)
        metric.http_status_code = response.status_code
        if pattern:
            matches = re.search(pattern, response.content)
            metric.pattern_found = bool(matches)
    except requests.exceptions.ConnectionError:
        metric.error_code = ErrorCodes.CONNECTION_ERROR
    except requests.exceptions.Timeout:
        metric.error_code = ErrorCodes.TIMEOUT
    except requests.exceptions.RequestException:
        metric.error_code = ErrorCodes.UNKNOWN_ERROR
    except Exception:
        metric.error_code = ErrorCodes.UNKNOWN_ERROR
        _log.warn("an unexpected error occurred", exc_info=True)
    finally:
        metric.http_response_time = int(time.time())

    return metric
