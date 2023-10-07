import sys

import autograder.api.common
import autograder.api.user.get

HEADERS = ['email', 'name', 'role']

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    config_data['email'] = arguments.email

    success, result = autograder.api.user.get.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    if (result is None):
        print("No matching user found.")
        return 0

    print("\t".join(HEADERS))

    row = [result[key] for key in HEADERS]
    print("\t".join([str(value) for value in row]))

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(
        description = 'Get a user in this course.',
        include_assignment = False)

    parser.add_argument('email', metavar = 'EMAIL',
        action = 'store', type = str,
        help = 'The email of the user to get.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
