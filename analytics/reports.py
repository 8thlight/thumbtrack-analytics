from functools import wraps

import pandas

from analytics import google
from analytics.config import VIEW_ID, RAILS_CONF_DATE_RANGE


REPORTS = []


def report(fn):
    """Appends the name of the wrapped function to REPORTS."""
    REPORTS.append(fn.__name__)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


@report
def sessions(analyticsreporting):
    request = {
        "viewId": VIEW_ID,
        "dateRanges": [RAILS_CONF_DATE_RANGE],
        "metrics": [{"expression": "ga:sessions"}],
        "dimensions": [{"name": "ga:date"}, {"name": "ga:hour"}],
    }
    response = google.get_report(analyticsreporting, request)
    report = response["reports"][0]
    data = google.parse_report(report)
    results = pandas.DataFrame(data, columns=["date", "hour", "metric", "value"])

    # convert datetime objects
    results.insert(0, "datetime", pandas.to_datetime(results.date + "-" + results.hour))
    results["datetime"] = results.datetime + pandas.Timedelta(
        "02:00:00"
    )  # convert to CST
    results["date"] = results.datetime.apply(lambda datetime: datetime.date())
    results["hour"] = results.datetime.apply(lambda datetime: datetime.hour)

    # remove "ga:" prefix from metric names
    results["metric"] = results.metric.str.strip("ga:")

    # label conference day
    conference_day_map = pandas.DataFrame(
        {
            "date": pandas.to_datetime(
                ["20190429", "20190430", "20190501", "20190502"]
            ),
            "conference_day": [-1, 1, 2, 3],
        }
    )
    conference_day_map["date"] = conference_day_map.date.apply(
        lambda datetime: datetime.date()
    )
    results = results.merge(conference_day_map)

    return results
