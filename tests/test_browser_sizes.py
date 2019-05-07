import pytest
from datatest import validate

import analytics


@pytest.fixture
def browser_sizes(google, analyticsreporting):
    google.parse_report.return_value = [
        ["desktop", "100x101", "ga:sessions", "1"],
        ["tablet", "90x91", "ga:sessions", "2"],
        ["mobile", "80x81", "ga:sessions", "3"],
        ["mobile", "(not set)", "ga:sessions", "4"],
    ]
    result = analytics.reports.browser_sizes(analyticsreporting)
    return result


def test_browser_sizes_has_data(browser_sizes):
    assert len(browser_sizes) > 0


def test_browser_sizes_columns(browser_sizes):
    validate(
        browser_sizes.columns,
        {"device", "dimensions", "width", "height", "metric", "value"},
    )


def test_browser_sizes_drops_bad_rows(browser_sizes):
    assert len(browser_sizes) == 3


def test_browser_sizes_extracts_width_and_height(browser_sizes):
    assert (browser_sizes.width == [100, 90, 80]).all()
