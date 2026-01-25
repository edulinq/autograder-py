# pylint: disable=invalid-name

import argparse
import sys

import autograder.cli.users.password.change as alias

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return alias.run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = alias._get_parser()
    parser.epilog = f"This is an alias for `{alias.__name__}`."
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
