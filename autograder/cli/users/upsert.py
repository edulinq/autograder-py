import sys

import autograder.api.config
import autograder.api.users.upsert
import autograder.cli.common
import autograder.cli.config

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

    autograder.cli.config.add_table_argument(parser)
    autograder.cli.config.add_skip_emails_argument(parser)

    autograder.cli.config.add_new_email_argument(parser, "upsert")
    autograder.cli.config.add_new_name_argument(parser, "upsert")
    autograder.cli.config.add_new_course_role_argument(parser, "upsert")
    autograder.cli.config.add_new_lms_id_argument(parser, "upsert")

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

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
