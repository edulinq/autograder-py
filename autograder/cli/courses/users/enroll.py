"""
Enroll a user in a course.
"""

import argparse
import sys

import edq.util.json

import autograder.api.courses.users.enroll
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.application_config

    config.raw_course_users = [
        {
            'email': config.new_email,
            'name': config.new_name,
            'course-role': config.new_course_role,
            'course-lms-id': config.new_lms_id,
        },
    ]

    result = autograder.api.courses.users.enroll.send(config, exit_on_error = True)
    print(edq.util.json.dumps(result, indent = 4))

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.users.enroll.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
