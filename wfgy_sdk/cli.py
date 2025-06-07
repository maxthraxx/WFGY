# wfgy_sdk/cli.py

import argparse
from .initializer import initialize
from .evaluator import evaluate

def main():
    parser = argparse.ArgumentParser(description="WFGY CLI")
    parser.add_argument("--init", action="store_true", help="Initialize demo data")
    parser.add_argument("--prompt", type=str, help="Input prompt for evaluation")
    args = parser.parse_args()

    if args.init:
        initialize()
        return

    if args.prompt:
        result = evaluate(args.prompt)
        print("Result:", result)
    else:
        print("Please provide a prompt using --prompt")
