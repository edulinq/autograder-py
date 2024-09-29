import sys

import autograder.api.courses.assignments.submissions.fetch.user.history
import autograder.cli.config
import autograder.submission

def run(arguments):
    result = autograder.api.courses.assignments.submissions.fetch.user.history.send(arguments,
            exit_on_error = True)

    if (not result['found-user']):
        print("No matching user found.")
        return 1

    history = result['history']

    if (not arguments.table):
        print("Found %d submissions." % (len(history)))
        for entry in history:
            print("    " + str(autograder.submission.SubmissionSummary.from_dict(entry)))

        return 0

    header = [
        'id',
        'score',
        'max_points',
        'grading_start_time',
        'message',
    ]

    print("\t".join(header))
    for entry in history:
        entry = autograder.submission.SubmissionSummary.from_dict(entry)
        entry = entry.to_dict()
        print("\t".join([str(entry[key]) for key in header]))

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.assignments.submissions.fetch.user.history._get_parser()

    autograder.cli.config.add_table_argument(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
