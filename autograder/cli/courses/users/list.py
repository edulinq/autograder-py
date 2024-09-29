import sys

import autograder.api.courses.users.list
import autograder.cli.common
import autograder.cli.config

def run(arguments):
    result = autograder.api.courses.users.list.send(arguments, exit_on_error = True)
    autograder.cli.common.list_users(result['users'], True, table = arguments.table)
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.users.list._get_parser()

    autograder.cli.config.add_table_argument(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
