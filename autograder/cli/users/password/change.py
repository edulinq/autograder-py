import sys

import autograder.api.error
import autograder.api.users.password.change

def run(arguments):
    result = autograder.api.users.password.change.send(arguments, exit_on_error = True)

    if result['duplicate']:
        print("Your new password must be different from your previous password.")
        return 0

    if result['success']:
        print("You have successfully changed your password.")
        return 0

    return 1

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.password.change._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
