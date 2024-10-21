import sys

import autograder.api.config
import autograder.api.metadata.describe
import autograder.cli.common
import autograder.cli.config

def run(arguments):
    result = autograder.api.metadata.describe.send(arguments, exit_on_error = True)
    autograder.cli.common.api_describe(result, table = arguments.table)
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.metadata.describe._get_parser()

    autograder.cli.config.add_table_argument(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
