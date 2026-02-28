"""
Get information about an assignment's Docker image (does not include the actual image).
"""

import argparse
import sys

import edq.util.json

import autograder.api.courses.assignments.images.info
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    result = autograder.api.courses.assignments.images.info.send(config, exit_on_error = True)
    print(edq.util.json.dumps(result['image-info'], indent = 4))
    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.images.info.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
