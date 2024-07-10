import sys

import autograder.api.users.tokens.create

def run(arguments):
    result = autograder.api.users.tokens.create.send(arguments, exit_on_error = True)

    print("Token ID: " + result['token-id'])
    print("Token Text: " + result['token-cleartext'])
    print("")
    print("Copy down the token text and keep it safe, this will be the only time it is ever shown.")

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.tokens.create._get_parser()

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
