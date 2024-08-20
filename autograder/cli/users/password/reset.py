import sys

import autograder.api.users.password.reset

def run(arguments):
    autograder.api.users.password.reset.send(arguments, exit_on_error = True)
    print("The server has successfully processed your request.")
    print("Check your email for the new password.")
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.password.reset._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
