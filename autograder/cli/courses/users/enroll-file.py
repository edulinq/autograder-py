import sys

import autograder.api.constants
import autograder.api.courses.users.enroll
import autograder.cli.common
import autograder.cli.config
import autograder.util.hash
import autograder.util.load

def run(arguments):
    arguments = vars(arguments)

    arguments['raw-course-users'] = _load_users(arguments['path'])
    arguments['send-emails'] = not arguments['skip-emails']

    result = autograder.api.courses.users.enroll.send(arguments, exit_on_error = True)

    autograder.cli.common.list_user_op_responses(result['results'], table = arguments['table'])
    return 0

def _load_users(path):
    users = []

    rows = autograder.util.load.load_tsv(path, 4)
    for lineno in range(len(rows)):
        row = rows[lineno]

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

        if (course_role not in autograder.api.constants.COURSE_ROLES):
            raise ValueError(
                "File ('%s') line (%d) has an invalid course role '%s'." % (
                    path, lineno, course_role))

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

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.users.enroll._get_parser()

    parser.description = ('Enroll users to the course from a TSV file.')

    autograder.cli.config.add_table_argument(parser)
    autograder.cli.config.add_skip_emails_argument(parser)

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file where each line contains up to four columns:'
                + ' [email, name, course-role, lms-id].'
                + ' Only the email is required. Leading and trailing whitespace is stripped'
                + ' from all fields.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
