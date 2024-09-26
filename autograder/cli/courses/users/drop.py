import sys

import autograder.api.courses.users.drop

def run(arguments):
    result = autograder.api.courses.users.drop.send(arguments, exit_on_error = True)

    if (not result['found-user']):
        print("User not found.")
        return 1

    print("User dropped.")
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.users.drop._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
