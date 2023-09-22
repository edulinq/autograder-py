import sys

import autograder.api.common
import autograder.api.submit

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    success, result = autograder.api.submit.send(arguments.server, config_data, arguments.files)

    if (not success):
        print(result)
        return 1

    print('The autograder successfully graded your assignment.')
    print(result.report())

    return 0

def main():
    return run(autograder.api.common.get_argument_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
