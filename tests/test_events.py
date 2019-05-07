import pytest
from datatest import validate

import analytics


@pytest.fixture
def events(google, analyticsreporting):
    google.parse_report.return_value = [
        [
            "ToggleOpen",
            "User Twirled Down Events",
            "20190429",
            "02",
            "ga:totalEvents",
            "10",
        ],
        ["Swipe", "User Swiped a Card", "20190429", "02", "ga:totalEvents", "10"],
        ["Pin", "Toggled the Pin", "20190429", "02", "ga:totalEvents", "10"],
        ["Outbound Link", "click", "20190429", "02", "ga:totalEvents", "10"],
        [
            "DayButton",
            "User Changed Day View",
            "20190429",
            "02",
            "ga:totalEvents",
            "10",
        ],
    ]
    result = analytics.reports.events(analyticsreporting)
    return result


def test_events_has_data(events):
    assert len(events) > 0


def test_events_has_columns(events):
    validate(
        events.columns,
        {
            "category",
            "action",
            "datetime",
            "date",
            "hour",
            "metric",
            "value",
            "conference_day",
        },
    )
