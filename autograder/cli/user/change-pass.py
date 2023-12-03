import sys

import autograder.api.user.changepass

def run(arguments):
    result = autograder.api.user.changepass.send(arguments, exit_on_error = True)

    if (not result['found-user']):
        print("User not found.")
        return 0

    print("Password changed.")
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.user.changepass._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
