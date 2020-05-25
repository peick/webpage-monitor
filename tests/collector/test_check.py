import requests.exceptions
import flexmock
import pytest
from freezegun import freeze_time

from webpage_monitor.model import ErrorCodes, WebpageMetric
from webpage_monitor.collector.check import check


@pytest.mark.parametrize(
    "exc, expect_error_code",
    [
        (requests.exceptions.ConnectionError(), ErrorCodes.CONNECTION_ERROR,),
        (requests.exceptions.RequestException(), ErrorCodes.UNKNOWN_ERROR,),
        (Exception("Unexpected exception."), ErrorCodes.UNKNOWN_ERROR,),
    ],
)
def test_check_exceptions(exc, expect_error_code):
    expect_metric = WebpageMetric(dict(
        http_response_time=1,
        http_status_code=None,
        error_code=expect_error_code,
        pattern_found=None,
    ))

    flexmock(requests).should_receive("get").and_raise(exc)

    with freeze_time("1970-01-01 00:00:01"):
        metric = check("http://some-url.com")

    assert metric == expect_metric


def test_check_without_pattern():
    expect_metric = WebpageMetric(dict(
        http_response_time=1,
        http_status_code=200,
        error_code=None,
        pattern_found=None,
    ))

    requests_response = flexmock(status_code=200)
    flexmock(requests).should_receive("get").and_return(requests_response)

    with freeze_time("1970-01-01 00:00:01"):
        metric = check("http://some-url.com")

    assert metric == expect_metric


@pytest.mark.parametrize(
    "pattern, matches",
    [
        (".*", True),
        ("foo", False),
        ("Dolor", True),
    ],
)
def test_check_pattern(pattern, matches):
    expect_metric = WebpageMetric(dict(
        http_response_time=1,
        http_status_code=200,
        error_code=None,
        pattern_found=matches,
    ))

    requests_response = flexmock(status_code=200, content=b"Lorem Ipsum Dolor")
    flexmock(requests).should_receive("get").and_return(requests_response)

    with freeze_time("1970-01-01 00:00:01"):
        metric = check("http://some-url.com", pattern=pattern)

    assert metric == expect_metric
