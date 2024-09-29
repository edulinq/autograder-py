import sys

import autograder.api.constants
import autograder.api.users.upsert
import autograder.cli.common
import autograder.cli.config
import autograder.util.hash
import autograder.util.load

def run(arguments):
    arguments = vars(arguments)

    arguments['raw-users'] = _load_users(arguments['path'])
    arguments['send-emails'] = not arguments['skip-emails']

    result = autograder.api.users.upsert.send(arguments, exit_on_error = True)

    autograder.cli.common.list_user_op_responses(result['results'], table = arguments['table'])
    return 0

def _load_users(path):
    users = []

    rows = autograder.util.load.load_tsv(path, 7)
    for lineno in range(len(rows)):
        row = rows[lineno]

        email = row.pop(0)

        password = ''
        if (len(row) > 0):
            password = row.pop(0)
            if (password != ''):
                password = autograder.util.hash.sha256_hex(password)

        name = ''
        if (len(row) > 0):
            name = row.pop(0)

        role = 'user'
        if (len(row) > 0):
            role = row.pop(0)
            role = role.lower()

        if (role not in autograder.api.constants.SERVER_ROLES):
            raise ValueError(
                "File ('%s') line (%d) has an invalid role '%s'." % (
                    path, lineno, role))

        course = ''
        if (len(row) > 0):
            course = row.pop(0)

        course_role = 'unknown'
        if (len(row) > 0):
            course_role = row.pop(0)
            course_role = course_role.lower()

        if (course_role not in autograder.api.constants.COURSE_ROLES):
            raise ValueError(
                "File ('%s') line (%d) has an invalid course role '%s'." % (
                    path, lineno, course_role))

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

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.upsert._get_parser()

    parser.description = ('Upsert users to the course from a TSV file.'
                + ' (Update if exists, otherwiese insert).')

    autograder.cli.config.add_table_argument(parser)
    autograder.cli.config.add_skip_emails_argument(parser)

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
