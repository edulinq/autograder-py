"""
Upsert a server user.
"""

import argparse
import sys

import edq.util.json

import autograder.api.users.upsert
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.application_config

    config.raw_server_users = [
        {
            'email': config.new_email,
            'pass': config.new_pass,
            'name': config.new_name,
            'role': config.new_role,
            'course': config.new_course,
            'course-role': config.new_course_role,
            'course-lms-id': config.new_lms_id,
        },
    ]

    result = autograder.api.users.upsert.send(config, exit_on_error = True)
    print(edq.util.json.dumps(result, indent = 4))

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.users.upsert.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
