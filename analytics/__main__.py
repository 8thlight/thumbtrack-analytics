import sys
import argparse

import analytics.google
import analytics.reports

parser = argparse.ArgumentParser()
parser.add_argument("report", nargs="*", help="one or more report names")
parser.add_argument("--all", "-a", help="run all reports", action="store_true")
parser.add_argument("--list", "-l", help="list available reports", action="store_true")
parser.add_argument("--print", "-p", help="print report to stdout", action="store_true")
args = parser.parse_args()

if args.list:
    print("Available reports:")
    for report_name in analytics.reports.REPORTS:
        print(f"- {report_name}")
    sys.exit(0)

report_names = analytics.reports.REPORTS if args.all else args.report

if len(report_names) == 0:
    print('Must provide a report name, or pass "--all". Available reports:')
    for report_name in analytics.reports.REPORTS:
        print(f"- {report_name}")

    sys.exit(1)

for report in report_names:
    if report not in analytics.reports.REPORTS:
        print(f'Report "{report}" not found. Available reports:')
        for report_name in analytics.reports.REPORTS:
            print(f"- {report_name}")

        sys.exit(1)


analyticsreporting = analytics.google.initialize_analyticsreporting()

for report in report_names:
    print(f"Running report {{ {report} }}")
    report_fn = getattr(analytics.reports, report)
    result = report_fn(analyticsreporting)
    dst = f"data/{report}.csv" if not args.print else sys.stdout
    result.to_csv(dst, index=False)
