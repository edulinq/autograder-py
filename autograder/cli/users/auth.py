import http
import sys

import autograder.api.error
import autograder.api.users.auth

def run(arguments):
    try:
        autograder.api.users.auth.send(arguments, exit_on_error = False)
    except autograder.api.error.APIError as ex:
        if (ex.code != http.HTTPStatus.UNAUTHORIZED):
            raise ex

        print("Authentication failed.")
        return 0

    print("Authentication successful.")
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.auth._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
