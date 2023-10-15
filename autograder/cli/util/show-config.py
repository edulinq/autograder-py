import sys

import autograder.api.common
import autograder.api.peek
import autograder.submission

HEADERS = ['key', 'value', 'source']

def run(arguments):
    config_data, sources = autograder.api.common.parse_config(arguments, show_sources = True)

    print("\t".join(HEADERS))

    for key in sorted(config_data.keys()):
        value = config_data[key]
        if (key == 'pass'):
            value = '*** password omitted ***'

        row = [key, value, sources[key]]
        print("\t".join([str(value) for value in row]))

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(description =
            'Show all the config values and where those values came from.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
