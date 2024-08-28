import sys

import autograder.api.courses.assignments.submissions.fetch.course.attempts
import autograder.cli.courses.assignments.submissions.common

def run(arguments):
    result = autograder.api.courses.assignments.submissions.fetch.course.attempts.send(arguments,
            exit_on_error = True)

    count = 0
    for (email, grading_result) in result['grading-results'].items():
        if (grading_result is None):
            continue

        autograder.cli.courses.assignments.submissions.common.output_grading_result(grading_result,
                arguments.out_dir)
        count += 1

    print("Wrote %d submissions to '%s'." % (count, arguments.out_dir))

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.assignments.submissions.fetch.course.attempts._get_parser()

    parser.add_argument('-o', '--out-dir', dest = 'out_dir',
        action = 'store', type = str, default = '.',
        help = ('Where to create a new directory that contains the submission information.'
            + ' Any existing subdirectories will be removed.'
            + ' Defaults to the current directory.'))

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
