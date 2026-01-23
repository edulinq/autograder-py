# pylint: disable=invalid-name

"""
Run a grader against multiple test assignments and ensure the output matches the expected output.
"""

import argparse
import sys
import traceback

import autograder.cli.parser
import autograder.submission

DEFAULT_ASSIGNMENT = 'assignment.json'

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    try:
        test_submissions = autograder.submission.fetch_test_submissions(args.submissions)
    except Exception as ex:
        print(f"Failed to load submission(s) from '{args.submissions}': '{ex}'.")
        traceback.print_exc()
        return 101

    errors = 0
    for test_submission in test_submissions:
        success = False

        try:
            success = autograder.submission.run_test_submission(args.assignment, test_submission)
        except Exception as ex:
            print(f"Failed to run submission '{test_submission}': '{ex}'.")
            traceback.print_exc()

        if (not success):
            errors += 1

    print(f"Encountered {errors} error(s) while testing {len(test_submissions)} submissions.")

    if (errors > 0):
        print("Faiure")
    else:
        print("Success")

    return errors

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    parser = autograder.cli.parser.get_parser(__doc__.strip())

    parser.add_argument('-a', '--assignment',
        action = 'store', type = str, required = False, default = DEFAULT_ASSIGNMENT,
        help = 'The path to a JSON file describing an assignment (default: %(default)s).')

    parser.add_argument('-s', '--submissions',
        action = 'store', type = str, required = True,
        help = 'The path to a dir containing one or more test submissions.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
