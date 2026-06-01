"""
Request a password reset.
"""

import argparse
import sys

import autograder.api.users.password.reset
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.config

    autograder.api.users.password.reset.send(config, exit_on_error = True)
    print("The server has successfully processed your request.")
    print("Check your email for the new password.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.users.password.reset.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
