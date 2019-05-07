from functools import wraps

import pandas

from analytics import google, utils
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
    results = utils.convert_date_hour_to_cst_datetime(results)
    results["metric"] = utils.parse_metric_name(results.metric)
    results = utils.label_conference_day(results)
    return results


@report
def devices(analyticsreporting):
    request = {
        "viewId": VIEW_ID,
        "dateRanges": [RAILS_CONF_DATE_RANGE],
        "metrics": [{"expression": "ga:users"}],
        "dimensions": [{"name": "ga:deviceCategory"}],
    }
    response = google.get_report(analyticsreporting, request)
    report = response["reports"][0]
    data = google.parse_report(report)
    results = pandas.DataFrame(data, columns=["device", "metric", "value"])
    results["metric"] = utils.parse_metric_name(results.metric)
    return results


@report
def browser_sizes(analyticsreporting):
    request = {
        "viewId": VIEW_ID,
        "dateRanges": [RAILS_CONF_DATE_RANGE],
        "metrics": [{"expression": "ga:sessions"}],
        "dimensions": [{"name": "ga:deviceCategory"}, {"name": "ga:browserSize"}],
    }
    response = google.get_report(analyticsreporting, request)
    report = response["reports"][0]
    data = google.parse_report(report)
    results = pandas.DataFrame(
        data, columns=["device", "dimensions", "metric", "value"]
    )
    results["metric"] = utils.parse_metric_name(results.metric)

    # extract width and height dimensions
    dimensions = results.dimensions.str.split("x", expand=True)
    dimensions.columns = ["width", "height"]
    dimensions = dimensions.loc[
        (dimensions.width.str.isnumeric()) & (dimensions.height.str.isnumeric()), :
    ].astype(int)
    results = results.merge(dimensions, left_index=True, right_index=True)
    results.dropna(subset=["width", "height"], inplace=True)

    return results


@report
def events(analyticsreporting):
    request = {
        "viewId": VIEW_ID,
        "dateRanges": [RAILS_CONF_DATE_RANGE],
        "metrics": [{"expression": "ga:totalEvents"}],
        "dimensions": [
            {"name": "ga:eventCategory"},
            {"name": "ga:eventAction"},
            {"name": "ga:date"},
            {"name": "ga:hour"},
        ],
    }
    response = google.get_report(analyticsreporting, request)
    report = response["reports"][0]
    data = google.parse_report(report)
    results = pandas.DataFrame(
        data, columns=["category", "action", "date", "hour", "metric", "value"]
    )
    results = utils.convert_date_hour_to_cst_datetime(results)
    results["metric"] = utils.parse_metric_name(results.metric)
    results = utils.label_conference_day(results)
    return results


@report
def new_users(analyticsreporting):
    request = {
        "viewId": VIEW_ID,
        "dateRanges": [RAILS_CONF_DATE_RANGE],
        "metrics": [{"expression": "ga:newUsers"}],
        "dimensions": [{"name": "ga:date"}, {"name": "ga:hour"}],
    }
    response = google.get_report(analyticsreporting, request)
    report = response["reports"][0]
    data = google.parse_report(report)
    results = pandas.DataFrame(data, columns=["date", "hour", "metric", "value"])
    results = utils.convert_date_hour_to_cst_datetime(results)
    results = utils.label_conference_day(results)
    return results


def duration(analyticsreporting):
    pass


def site_speed(analyticsreporting):
    pass
