"""
List the users on the server.
"""

import argparse
import sys

import autograder.api.users.list
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    result = autograder.api.users.list.send(config)

    # TEST
    print(result)

    ''' TEST
    output = lms.model.base.base_list_to_output_format(users, args.output_format,
            skip_headers = args.skip_headers,
            pretty_headers = args.pretty_headers,
            include_extra_fields = args.include_extra_fields,
    )
    print(output)
    '''

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser():
    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.users.list.API_PARAMS,
        include_output_format = True)

    return parser

''' TEST
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
'''

if (__name__ == '__main__'):
    sys.exit(main())
