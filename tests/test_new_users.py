from datetime import datetime

import pytest
from datatest import validate

import analytics


@pytest.fixture
def new_users(google, analyticsreporting):
    google.parse_report.return_value = [
        ["20190429", "01", "ga:newUsers", "2"],
        ["20190429", "23", "ga:newUsers", "10"],
    ]
    result = analytics.reports.new_users(analyticsreporting)
    return result


def test_new_users_has_data(new_users):
    assert len(new_users) > 0


def test_new_users_has_columns(new_users):
    validate(
        new_users.columns,
        {"datetime", "date", "hour", "metric", "value", "conference_day"},
    )


def test_new_users_has_datetime(new_users):
    validate(new_users.datetime, datetime)
