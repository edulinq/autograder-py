import sys

import autograder.api.courses.users.get
import autograder.cli.common

def run(arguments):
    result = autograder.api.courses.users.get.send(arguments, exit_on_error = True)

    if (not result['found']):
        print("User not found.")
        return 1

    autograder.cli.common.list_users([result['user']], True, table = arguments.table)
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.users.get._get_parser()

    parser.add_argument('--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
