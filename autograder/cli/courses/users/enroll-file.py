import sys

import autograder.api.constants
import autograder.api.courses.users.enroll
import autograder.cli.common
import autograder.util.hash

def run(arguments):
    arguments = vars(arguments)

    arguments['raw-course-users'] = _load_users(arguments['path'])
    arguments['send-emails'] = not arguments['skip-emails']

    result = autograder.api.courses.users.enroll.send(arguments, exit_on_error = True)

    autograder.cli.common.list_user_op_responses(result['results'], table = arguments['table'])
    return 0

def _load_users(path):
    users = []

    with open(path, 'r') as file:
        lineno = 0
        for line in file:
            lineno += 1

            line = line.strip()
            if (line == ""):
                continue

            parts = line.split("\t")
            parts = [part.strip() for part in parts]

            if (len(parts) > 4):
                raise ValueError(
                    "File ('%s') line (%d) has too many values. Max is 4, found %d." % (
                        path, lineno, len(parts)))

            email = parts.pop(0)

            name = ''
            if (len(parts) > 0):
                name = parts.pop(0)

            course_role = ''
            if (len(parts) > 0):
                course_role = parts.pop(0)
                course_role = course_role.lower()

            if (course_role == ''):
                course_role = 'unknown'

            if (course_role not in autograder.api.constants.COURSE_ROLES):
                raise ValueError(
                    "File ('%s') line (%d) has an invalid course role '%s'." % (
                        path, lineno, course_role))

            course_lms_id = ''
            if (len(parts) > 0):
                course_lms_id = parts.pop(0)

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

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file where each line contains up to four columns:'
                + ' [email, name, course-role, lms-id].'
                + ' Only the email is required. Leading and trailing whitespace is stripped'
                + ' from all fields.')

    parser.add_argument('--skip-emails', dest = 'skip-emails',
        action = 'store_true', default = False,
        help = 'Skip sending any emails. Be aware that this may result in inaccessible'
                + ' information (default: %(default)s).')

    parser.add_argument('--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())