"""
Remove a specified submission.
Defaults to the most recent submission.
"""

import argparse
import sys

import autograder.api.courses.assignments.submissions.remove
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    found_user, found_submission = autograder.api.courses.assignments.submissions.remove.send(config, exit_on_error = True)

    if (not found_user):
        print(f"No matching user found: '{config.get('target_email', '')}'.", file = sys.stderr)
        return 1

    if (not found_submission):
        print(f"No matching submission found: '{config.get('target_submission', '')}'.", file = sys.stderr)
        return 2

    print("Submission removed.")
    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.submissions.remove.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
