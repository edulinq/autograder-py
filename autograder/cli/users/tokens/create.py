"""
Create a new token.
"""

import argparse
import sys

import autograder.api.users.tokens.create
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.config

    result = autograder.api.users.tokens.create.send(config, exit_on_error = True)

    print("Token ID: " + result['token-info']['id'])
    print("Token Text: " + result['token-cleartext'])
    print("")
    print("Copy down the token text and keep it safe, this will be the only time it is ever shown.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.users.tokens.create.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
