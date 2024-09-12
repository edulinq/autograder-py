import sys

import autograder.api.config
import autograder.api.users.upsert
import autograder.cli.common

def run(arguments):
    arguments = vars(arguments)

    password = arguments['new-pass']
    if (password != ''):
        password = autograder.util.hash.sha256_hex(password)

    arguments['raw-users'] = [{
        'email': arguments['new-email'],
        'name': arguments['new-name'],
        'role': arguments['new-role'],
        'pass': password,
        'course': arguments['new-course'],
        'course-role': arguments['new-course-role'],
        'course-lms-id': arguments['new-lms-id'],
    }]

    arguments['send-emails'] = not arguments['skip-emails']

    result = autograder.api.users.upsert.send(arguments, exit_on_error = True)

    autograder.cli.common.list_user_op_responses(result['results'], table = arguments['table'])
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.upsert._get_parser()

    parser.add_argument('--skip-emails', dest = 'skip-emails',
        action = 'store_true', default = False,
        help = 'Skip sending any emails. Be aware that this may result in inaccessible'
        + ' information (default: %(default)s).')

    parser.add_argument('--new-email', dest = 'new-email',
        action = 'store', type = str, required = True,
        help = 'The email of the user to upsert.')

    parser.add_argument('--new-name', dest = 'new-name',
        action = 'store', type = str, default = '',
        help = 'The name of the user to upsert.')

    parser.add_argument('--new-role', dest = 'new-role',
        action = 'store', type = str, default = 'user',
        choices = autograder.api.constants.SERVER_ROLES,
        help = 'The role of the user to upsert (default: %(default)s).')

    parser.add_argument('--new-pass', dest = 'new-pass',
        action = 'store', type = str, default = '',
        help = 'The password of the user to upsert.'
            + ' If empty, the server will generate and email a password.')

    parser.add_argument('--new-course', dest = 'new-course',
        action = 'store', type = str, default = '',
        help = 'The course of the user to upsert.')

    parser.add_argument('--new-course-role', dest = 'new-course-role',
        action = 'store', type = str, default = 'student',
        choices = autograder.api.constants.COURSE_ROLES,
        help = 'The course role of the user to upsert (default: %(default)s).')

    parser.add_argument('--new-lms-id', dest = 'new-lms-id',
        action = 'store', type = str, default = '',
        help = 'The lms id of the user to upsert.')

    parser.add_argument('--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
