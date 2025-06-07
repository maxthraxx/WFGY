# wfgy_sdk/cli.py

import argparse
from .initializer import initialize
from .evaluator import run_benchmarks
from .reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="WFGY 1.0 CLI")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init", help="Download data and weights")
    ev = sub.add_parser("evaluate", help="Run evaluation suites")
    ev.add_argument("--suite", default="all", help="Suite name or comma list")
    rp = sub.add_parser("report", help="Generate summary report")
    rp.add_argument("--format", choices=["html","md"], default="html")
    rp.add_argument("--output", default="wfgy_results/report.html")

    args = parser.parse_args()
    if args.cmd == "init":
        initialize()
    elif args.cmd == "evaluate":
        suites = args.suite.split(",")
        run_benchmarks(suites)
    elif args.cmd == "report":
        generate_report(args.format, args.output)
    else:
        parser.print_help()
