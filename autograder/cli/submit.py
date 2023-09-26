import sys

import autograder.api.common
import autograder.api.submit

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    config_data['message'] = arguments.message

    success, result = autograder.api.submit.send(arguments.server, config_data, arguments.files)

    if (not success):
        print(result)
        return 1

    print('The autograder successfully graded your assignment.')
    print(result.report())

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(description = 'Submit an assignment.')

    parser.add_argument('--message', dest = 'message',
        action = 'store', type = str, default = '',
        help = 'message')

    parser.add_argument('files', metavar = 'FILE',
        action = 'store', type = str, nargs = '+',
        help = 'The path to your submission file.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
