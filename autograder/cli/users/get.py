import sys

import autograder.api.users.get
import autograder.cli.common
import autograder.cli.config

def run(arguments):
    result = autograder.api.users.get.send(arguments, exit_on_error = True)

    if (not result['found']):
        print("User not found.")
        return 1

    autograder.cli.common.list_users([result['user']], False, table = arguments.table,
        normalize = arguments.normalize)
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.get._get_parser()

    autograder.cli.config.add_table_argument(parser)

    parser.add_argument('--normalize', dest = 'normalize',
        action = 'store_true', default = False,
        help = 'Normalize the TSV table to include at most one course enrollment per line. If the'
            + ' user is enrolled in multiple courses, they will appear multiple times. Each line'
            + ' contains the following columns: [email, name, role, course-id, course-name,'
            + ' course-role]. Only applies if --table is set (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
