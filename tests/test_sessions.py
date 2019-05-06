from datetime import datetime

import pytest
from datatest import validate

import analytics.reports


@pytest.fixture
def sessions(google, analyticsreporting):
    google.parse_report.return_value = [
        ["20190429", "01", "ga:sessions", "2"],
        ["20190429", "23", "ga:sessions", "10"],
    ]
    result = analytics.reports.sessions(analyticsreporting)
    return result


def test_sessions_has_data(sessions):
    assert len(sessions) > 0


def test_sessions_has_datetime(sessions):
    validate(sessions.datetime, datetime)


def test_sessions_parses_metric_name(sessions):
    validate(sessions.metric, "sessions")


def test_sessions_labels_conference_day(sessions):
    validate(sessions.conference_day.values, {-1, 1})


def test_sessions_coverts_hours_to_cst(sessions):
    validate(sessions.hour.values, {3, 1})
