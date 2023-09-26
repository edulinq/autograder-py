import sys

import autograder.api.common
import autograder.api.peek
import autograder.submission

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    success, result = autograder.api.peek.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    if (result is None):
        print("No past submission found for this assignment.")
        return 0

    print('Found a past submission for this assignment.')
    print(result.report())

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(description =
            'Peek the most recent submission for this assignment.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
