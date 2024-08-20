import sys

import autograder.api.courses.assignments.submissions.fetch.course.scores

HEADER = [
    'email', 'has_submission', 'short-id', 'score', 'grading_start_time', 'message',
]

def run(arguments):
    result = autograder.api.courses.assignments.submissions.fetch.course.scores.send(arguments,
            exit_on_error = True)

    print("\t".join(HEADER))

    for (email, submission) in sorted(result['submission-infos'].items()):
        row = [email, (submission is not None)]

        if (submission is None):
            row += ([''] * 4)
        else:
            row += [submission[key] for key in HEADER[2:]]

        print("\t".join(map(str, row)))

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.assignments.submissions.fetch.course.scores._get_parser()
    return parser

if (__name__ == '__main__'):
    sys.exit(main())
