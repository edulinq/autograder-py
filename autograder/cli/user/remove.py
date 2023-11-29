import sys

import autograder.api.user.remove

def run(arguments):
    result = autograder.api.user.remove.send(arguments, exit_on_error = True)

    if (result['found-user']):
        print("User removed.")
    else:
        print("User not found.")

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.user.remove._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
