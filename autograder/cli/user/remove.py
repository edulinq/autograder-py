import sys

import autograder.api.common
import autograder.api.user.remove

KEY_FOUND_USER = 'found-user'

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    config_data['email'] = arguments.email

    success, result = autograder.api.user.remove.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    if (not result[KEY_FOUND_USER]):
        print("No matching user found.")
        return 0

    print("User removed.")

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(
        description = 'Authenticate as a user in this course.',
        include_assignment = False)

    parser.add_argument('email', metavar = 'EMAIL',
        action = 'store', type = str,
        help = 'The email of the user to remove.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
