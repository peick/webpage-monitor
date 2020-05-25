import pytest

from webpage_monitor import model


@pytest.mark.parametrize("data", [
    None,
    "",
    "\"",
    "{}",
    "{\"http_response_time\": null}",
])
def test_from_json_invalid(data):
    with pytest.raises(ValueError):
        model.from_json(data)


@pytest.mark.parametrize("data", [
    "{\"http_response_time\": 1}"
])
def test_from_json_valid(data):
    model.from_json(data)
