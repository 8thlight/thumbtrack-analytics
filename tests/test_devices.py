import pytest
from datatest import validate

import analytics


@pytest.fixture
def devices(google, analyticsreporting):
    google.parse_report.return_value = [
        ["desktop", "ga:users", "100"],
        ["mobile", "ga:users", "100"],
        ["tablet", "ga:users", "100"],
    ]
    result = analytics.reports.devices(analyticsreporting)
    return result


def test_devices_has_data(devices):
    assert len(devices) > 0


def test_devices_has_columns(devices):
    validate(devices.columns, {"device", "metric", "value"})


def test_devices_parses_metric_name(devices):
    validate(devices.metric, "users")
