import sys

import autograder.api.common
import autograder.api.history
import autograder.submission

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    success, result = autograder.api.history.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    if (len(result) == 0):
        print("No submissions found.")
        return 0

    print("Found %d submissions." % (len(result)))
    for entry in result:
        print("    " + str(autograder.submission.SubmissionSummary.from_dict(entry)))

    return 0

def _load_args():
    parser = autograder.api.common.get_argument_parser(description =
            'Get a history of past submission for this assignment.')

    return parser.parse_args()

def main():
    return run(_load_args())

if (__name__ == '__main__'):
    sys.exit(main())
