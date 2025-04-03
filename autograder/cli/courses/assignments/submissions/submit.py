import sys

import autograder.api.courses.assignments.submissions.submit
import autograder.cli.common
import autograder.cli.config

def run(arguments):
    result = autograder.api.courses.assignments.submissions.submit.send(arguments,
            files = arguments.files, exit_on_error = True)

    return autograder.cli.common.display_grading_result(result)

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.assignments.submissions.submit._get_parser()

    autograder.cli.config.add_submission_files_argument(parser)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
