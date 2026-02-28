# pylint: disable=invalid-name

"""
Enroll users from a TSV file into a course.
"""

import argparse
import sys
import typing

import edq.util.json

import autograder.api.config
import autograder.api.courses.users.enroll
import autograder.cli.parser
import autograder.util.load

API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_COURSE,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_DRY_RUN,
    autograder.api.config.PARAM_SKIP_INSERTS,
    autograder.api.config.PARAM_SKIP_UPDATES,

    autograder.api.config.PARAM_SEND_EMAILS,

    autograder.api.config.PARAM_RAW_COURSE_USERS,
]

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config
    config['raw_course_users'] = _load_users(args.path)

    result = autograder.api.courses.users.enroll.send(config, exit_on_error = True)
    print(edq.util.json.dumps(result, indent = 4))

    return 0

def _load_users(path: str) -> typing.List[typing.Dict[str, str]]:
    """ Load raw user entries from a TSV file. """

    users = []

    rows = autograder.util.load.load_tsv(path, 4)
    for (lineno, row) in enumerate(rows):
        email = row.pop(0)

        name = ''
        if (len(row) > 0):
            name = row.pop(0)

        course_role = ''
        if (len(row) > 0):
            course_role = row.pop(0)
            course_role = course_role.lower()

        if (course_role == ''):
            course_role = 'unknown'

        if (not autograder.model.user.CourseRole.has_value(course_role)):
            raise ValueError(f"File ('{path}') line ({lineno}) has an invalid course role '{course_role}'.")

        course_lms_id = ''
        if (len(row) > 0):
            course_lms_id = row.pop(0)

        users.append({
            'email': email,
            'name': name,
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
        help = 'Path to a TSV file where each line contains up to four columns:'
                + ' [email, name, course-role, lms-id].'
                + ' Only the email is required. Leading and trailing whitespace is stripped'
                + ' from all fields.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
