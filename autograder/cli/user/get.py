import sys

import autograder.api.user.get

HEADERS = ['email', 'name', 'role', 'lms-id']

def run(arguments):
    result = autograder.api.user.get.send(arguments, exit_on_error = True)

    if (arguments.table):
        print("\t".join(HEADERS))
        if (not result['found-user']):
            return 0

        row = [result['user'][key] for key in HEADERS]
        print("\t".join([str(value) for value in row]))
    else:
        if (not result['found-user']):
            print("No matching user found.")
            return 0

        print("Email:", result['user']['email'])
        print("Name:", result['user']['name'])
        print("Role:", result['user']['role'])
        print("LMS ID:", result['user']['lms-id'])

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.user.get._get_parser()

    parser.add_argument('-t', '--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
