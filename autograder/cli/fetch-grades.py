import sys

import autograder.api.common
import autograder.api.fetchgrades
import autograder.submission

HEADERS = ['user', 'has_submission', 'score', 'max_points', 'id', 'time']

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    success, result = autograder.api.fetchgrades.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    if (len(result) == 0):
        print("No submissions found.")
        return 0

    print("\t".join(HEADERS))

    for (email, entry) in result.items():
        row = []

        if (entry is None):
            row = [email, False, None, None, None, None]
        else:
            summary = autograder.submission.SubmissionSummary.from_dict(entry)
            row = [
                email, True,
                summary.score, summary.max_points,
                summary.short_id(), summary.pretty_time()
            ]

        print("\t".join([str(element) for element in row]))

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(description =
            'Get all the most recent submissions for this assignment.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
