import sys

import autograder.api.lms.userget
import autograder.cli.common
import autograder.cli.config

def run(arguments):
    result = autograder.api.lms.userget.send(arguments, exit_on_error = True)

    if (not result['found-autograder-user']):
        print("No matching autograder user found.")
        return 0

    if (not result['found-lms-user']):
        print("No matching lms user found.")
        return 0

    autograder.cli.common.list_users([result['user']], True, table = arguments.table)
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.lms.userget._get_parser()

    autograder.cli.config.add_table_argument(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
