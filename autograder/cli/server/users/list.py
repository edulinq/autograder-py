import sys

import autograder.api.server.users.list
import autograder.api.config
import autograder.cli.common

def run(arguments):
    result = autograder.api.server.users.list.send(arguments, exit_on_error = True)
    autograder.cli.common.list_users(result['users'], False, table = arguments.table,
        expanded = arguments.expand)
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.server.users.list._get_parser()

    parser.add_argument('--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    parser.add_argument('--expand', dest = 'expand',
        action = autograder.api.config.CoupledAction, coupled_arg = 'table', default = False,
        help = 'Expand the TSV table for each course a user is enrolled in (default: %(default)s). \
                    Can only be used if --%(coupled_arg)s is set.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())