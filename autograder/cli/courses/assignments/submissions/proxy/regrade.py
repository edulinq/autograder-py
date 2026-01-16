"""
Proxy regrade an assignment for all target users using their most recent submission.
"""

import argparse
import sys

import edq.util.json

import autograder.api.courses.assignments.submissions.proxy.regrade
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    result = autograder.api.courses.assignments.submissions.proxy.regrade.send(config)
    print(edq.util.json.dumps(result, indent = 4))

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.submissions.proxy.regrade.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
