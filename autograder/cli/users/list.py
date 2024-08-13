import sys

import autograder.api.config
import autograder.api.users.list
import autograder.cli.common

def run(arguments):
    result = autograder.api.users.list.send(arguments, exit_on_error = True)
    autograder.cli.common.list_users(result['users'], False, table = arguments.table,
        normalize = arguments.normalize)
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.list._get_parser()

    parser.add_argument('--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    parser.add_argument('--normalize', dest = 'normalize',
        action = 'store_true', default = False,
        help = 'Normalize the TSV table for each course a user is enrolled in (default: \
                %(default)s). Can only be used if --table is set.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
