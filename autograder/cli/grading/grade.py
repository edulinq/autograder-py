"""
Grade an assignment (specified by an assignment JSON file) with the given submission.
Non-Python assignments can be graded, but they require an "invocation" field'
in the assignment config, and the running machine must be configured to run them'
(e.g. have all the required software installed).
"""

import argparse
import sys

import autograder.cmd.gradeassignment

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    return autograder.cmd.gradeassignment.run(args)

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    args, _ = _get_parser().parse_known_args()
    return run_cli(args)

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    return autograder.cmd.gradeassignment._get_parser()

if (__name__ == '__main__'):
    sys.exit(main())
