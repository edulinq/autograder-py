"""
Authenticate as a user.
"""

import argparse
import http
import sys

import autograder.api.users.auth
import autograder.cli.parser
import autograder.error

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.config

    try:
        autograder.api.users.auth.send(config, exit_on_error = False)
    except autograder.error.APIError as ex:
        if (ex.code != http.HTTPStatus.UNAUTHORIZED):
            raise ex

        print("Authentication failed.")
        return 1

    print("Authentication successful.")
    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.users.auth.API_PARAMS,
        include_output_format = True)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
