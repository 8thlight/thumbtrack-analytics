import sys
import argparse

import analytics.google
import analytics.reports

parser = argparse.ArgumentParser()
parser.add_argument("report", nargs="?")
parser.add_argument("--list", "-l", help="list available reports", action="store_true")
parser.add_argument(
    "--stdout", "-s", help="print report to stdout", action="store_true"
)
args = parser.parse_args()


if args.list:
    print("Available reports:")
    for report_name in analytics.reports.REPORTS:
        print(f"- {report_name}")
    sys.exit(0)


if args.report not in analytics.reports.REPORTS:
    print(f'Report "{args.report}" not found. Available reports:')
    for report_name in analytics.reports.REPORTS:
        print(f"- {report_name}")

    sys.exit(1)


analyticsreporting = analytics.google.initialize_analyticsreporting()
report_fn = getattr(analytics.reports, args.report)
result = report_fn(analyticsreporting)

dst = f"data/{args.report}.csv" if not args.stdout else sys.stdout
result.to_csv(dst, index=False)
