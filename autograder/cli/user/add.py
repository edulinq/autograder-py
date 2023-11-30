import sys

import autograder.api.constants
import autograder.api.user.add
import autograder.cli.common
import autograder.util.hash

def run(arguments):
    arguments = vars(arguments)

    password = arguments['new-pass']
    if (password != ''):
        password = autograder.util.hash.sha256_hex(password)

    arguments['new-users'] = [{
        'email': arguments['new-email'],
        'pass': password,
        'name': arguments['new-name'],
        'role': arguments['new-role'],
        'lms-id': arguments['new-lms-id'],
    }]

    result = autograder.api.user.add.send(arguments, exit_on_error = True)

    autograder.cli.common.list_add_users(result, table = arguments['table'])
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.user.add._get_parser()

    parser.description = ('Add a user to the course.'
            + ' When force is true, this becomes an upsert (update if exists, otherwise insert).')

    parser.add_argument('--new-email', dest = 'new-email',
        action = 'store', type = str, required = True,
        help = 'The email of the user to add.')

    parser.add_argument('--new-pass', dest = 'new-pass',
        action = 'store', type = str, default = '',
        help = 'The password of the user to add.'
            + ' If empty, the server will generate and email a password.')

    parser.add_argument('--new-name', dest = 'new-name',
        action = 'store', type = str, default = '',
        help = 'The name of the user to add.')

    parser.add_argument('--new-role', dest = 'new-role',
        action = 'store', type = str, default = 'unknown',
        choices = autograder.api.constants.ROLES,
        help = 'The role of the user to add (defaults to student).')

    parser.add_argument('--new-lms-id', dest = 'new-lms-id',
        action = 'store', type = str, default = '',
        help = 'Role of the user to add (defaults to student).')

    parser.add_argument('--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
