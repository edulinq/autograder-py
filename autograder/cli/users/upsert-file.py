# pylint: disable=invalid-name

"""
Upsert server users from a TSV file.
"""

import argparse
import sys
import typing

import edq.util.hash

import autograder.api.config
import autograder.api.model
import autograder.api.users.upsert
import autograder.cli.parser
import autograder.util.load

API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_SKIP_INSERTS,
    autograder.api.config.PARAM_SKIP_UPDATES,

    autograder.api.config.PARAM_SEND_EMAILS,

    autograder.api.config.PARAM_RAW_SERVER_USERS,
]

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config
    config['raw_users'] = _load_users(args.path)

    result = autograder.api.users.upsert.send(config)
    print(edq.util.json.dumps(result, indent = 4))

    return 0

def _load_users(path: str) -> typing.List[typing.Dict[str, str]]:
    """ Load raw user entries from a TSV file. """

    users = []

    rows = autograder.util.load.load_tsv(path, 7)
    for (lineno, row) in enumerate(rows):
        email = row.pop(0)

        password = ''
        if (len(row) > 0):
            password = row.pop(0)
            if (password != ''):
                password = edq.util.hash.sha256_hex(password)

        name = ''
        if (len(row) > 0):
            name = row.pop(0)

        role = 'user'
        if (len(row) > 0):
            role = row.pop(0)
            role = role.lower()

        if (not autograder.api.model.ServerRole.has_value(role)):
            raise ValueError(f"File ('{path}') line ({lineno}) has an invalid role '{role}'.")

        course = ''
        if (len(row) > 0):
            course = row.pop(0)

        course_role = 'unknown'
        if (len(row) > 0):
            course_role = row.pop(0)
            course_role = course_role.lower()

        if (not autograder.api.model.CourseRole.has_value(course_role)):
            raise ValueError(f"File ('{path}') line ({lineno}) has an invalid course role '{course_role}'.")

        course_lms_id = ''
        if (len(row) > 0):
            course_lms_id = row.pop(0)

        users.append({
            'email': email,
            'pass': password,
            'name': name,
            'role': role,
            'course': course,
            'course-role': course_role,
            'course-lms-id': course_lms_id,
        })

    return users

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        API_PARAMS)

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file where each line contains up to seven columns:'
                + ' [email, pass, name, role, course, course-role, lms-id].'
                + ' Only the email is required. Leading and trailing whitespace is stripped'
                + ' from all fields, including pass. If pass is empty, a password will be'
                + ' randomly generated and emailed to the user.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
