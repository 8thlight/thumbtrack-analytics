import pandas


def parse_metric_name(metrics):
    """Make GA metric names human-readable.

    Args:
        metrics (pandas.Series)
    Returns:
        pandas.Series
    """
    return metrics.str.strip("ga:")


def convert_date_hour_to_cst_datetime(results):
    """Convert date and hour strings to CST datetimes.

    Args:
        results (pandas.DataFrame): with string columns "date" and "hour"
    Returns:
        pandas.DataFrame with new column "datetime", and adjusted "date" and "hour" columns.
    """
    results.insert(0, "datetime", pandas.to_datetime(results.date + "-" + results.hour))
    results["datetime"] = results.datetime + pandas.Timedelta(
        "02:00:00"
    )  # convert to CST
    results["date"] = results.datetime.apply(lambda datetime: datetime.date())
    results["hour"] = results.datetime.apply(lambda datetime: datetime.hour)
    return results


def label_conference_day(results):
    """Label each date as a day of the conference.

    Args:
        results (pandas.DataFrame): with date column "date"
    Returns:
        pandas.DataFrame with new column "conference_day"
    """
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
