import sys

import autograder.api.config
import autograder.api.users.list
import autograder.cli.common
import autograder.cli.config

def run(arguments):
    result = autograder.api.users.list.send(arguments, exit_on_error = True)
    autograder.cli.common.list_users(result['users'], False, table = arguments.table,
        normalize = arguments.normalize)
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.list._get_parser()

    autograder.cli.config.add_table_argument(parser)

    parser.add_argument('--normalize', dest = 'normalize',
        action = 'store_true', default = False,
        help = 'Normalize the TSV table to include at most one course enrollment per line, users'
            + ' enrolled in multiple courses will appear multiple times. Each line contains the'
            + ' following columns: [email, name, role, course-id, course-name, course-role]. If'
            + ' a user is not enrolled in any courses, they will appear once with empty course'
            + ' information. Only applies if --table is set (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
