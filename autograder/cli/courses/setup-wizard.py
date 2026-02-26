# pylint: disable=invalid-name

"""
Run the course setup wizard.
"""

import argparse
import sys

import autograder.wizard.coursesetup.wizard
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    wizard = autograder.wizard.coursesetup.wizard.CourseSetupWizard(config)
    wizard.run()

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip())

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
