import sys

import autograder.api.users.tokens.delete

def run(arguments):
    result = autograder.api.users.tokens.delete.send(arguments, exit_on_error = True)

    if (not result['found']):
        print("Token not found.")
        return 1

    print("Token deleted.")
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.tokens.delete._get_parser()

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
