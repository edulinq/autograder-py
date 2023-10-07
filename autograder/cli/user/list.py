import sys

import autograder.api.common
import autograder.api.user.list

HEADERS = ['email', 'name', 'role']

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    success, result = autograder.api.user.list.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    if (len(result) == 0):
        print("No users found.")
        return 0

    print("\t".join(HEADERS))

    for user in result:
        row = [user[key] for key in HEADERS]
        print("\t".join([str(value) for value in row]))

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(
        description = 'Get the users in this course.',
        include_assignment = False)

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
