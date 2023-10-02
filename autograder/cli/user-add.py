import sys

import autograder.api.common
import autograder.api.user.add

KEY_SUCCESS = 'success'
KEY_FOUND_USER = 'found-user'

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)

    config_data['email'] = arguments.email
    config_data['new-pass'] = arguments.newpass
    config_data['name'] = arguments.name
    config_data['role'] = arguments.role
    config_data['force'] = arguments.force
    config_data['send-email'] = arguments.sendemail

    if ((arguments.newpass == '') and (not arguments.sendemail)):
        print("You must send an email if you do not specify a password.")
        return 1

    success, result = autograder.api.user.add.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    if (result['user-exists']):
        print("ERROR: User already exists and --force was not used.")
        return 1

    print("User added.")

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(
        description = 'Add a user to this course.',
        include_assignment = False)

    parser.add_argument('email', metavar = 'EMAIL',
        action = 'store', type = str,
        help = 'The email of the user to add.')

    parser.add_argument('--new-pass', dest = 'newpass',
        action = 'store', type = str, default = '',
        help = 'The password of the user to add.'
            + ' If empty, the server will generate a password'
            + ' (--send-email is required in this case).')

    parser.add_argument('--name', dest = 'name',
        action = 'store', type = str, default = '',
        help = 'Name of the user to add (defaults to the email).')

    parser.add_argument('--role', dest = 'role',
        action = 'store', type = str, default = 'student',
        help = 'Role of the user to add (defaults to student).')

    parser.add_argument('--force', dest = 'force',
        action = 'store_true', default = False,
        help = 'Overwrite any existing users (default: %(default)s).')

    parser.add_argument('--send-email', dest = 'sendemail',
        action = 'store_true', default = False,
        help = 'Send an email to the user being added.'
            + ' Required if a password is generated (default: %(default)s).')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
