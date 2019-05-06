from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from analytics.config import KEY_FILE_LOCATION


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES
    )

    # Build the service object.
    analytics = build("analyticsreporting", "v4", credentials=credentials)

    return analytics


def get_report(analytics, report_request):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    return (
        analytics.reports()
        .batchGet(body={"reportRequests": [report_request]})
        .execute()
    )


def parse_report(report):
    report_data = []

    columnHeader = report.get("columnHeader", {})
    dimensionHeaders = columnHeader.get("dimensions", [])
    metricHeaders = columnHeader.get("metricHeader", {}).get("metricHeaderEntries", [])

    for row in report.get("data", {}).get("rows", []):
        data = []
        dimensions = row.get("dimensions", [])
        dateRangeValues = row.get("metrics", [])

        for header, dimension in zip(dimensionHeaders, dimensions):
            data.append(dimension)

        for i, values in enumerate(dateRangeValues):
            for metricHeader, value in zip(metricHeaders, values.get("values")):
                data.extend([metricHeader.get("name"), value])

        report_data.append(data)

    return report_data
