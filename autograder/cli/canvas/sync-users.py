import sys

import autograder.api.common
import autograder.api.canvas.syncusers

KEY_COUNT = 'count'

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    success, result = autograder.api.canvas.syncusers.send(config_data.get("server"), config_data)

    if (not success):
        print(result)
        return 1

    print("Synced %d users." % (result[KEY_COUNT]))
    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(
        description = 'Sync canvas user IDs to local autograder users',
        include_assignment = False)

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
