"""
Grade an assignment (specified by an assignment JSON file) with the given submission.
Non-Python assignments can be graded, but they require an "invocation" field'
in the assignment config, and the running machine must be configured to run them'
(e.g. have all the required software installed).
"""

import argparse
import json
import os
import sys

import edq.util.json

import autograder.cli.parser
import autograder.submission

DEFAULT_ASSIGNMENT: str = 'assignment.json'
TEST_SUBMISSION_FILENAME: str = 'test-submission.json'

def run(args: argparse.Namespace) -> int:
    """
    Grade an assignment, output the report, and optionally output additional out or test files.
    """

    assignment_config_path = os.path.abspath(args.assignment)
    submission_path = os.path.abspath(args.submission)

    grading_dir = autograder.submission.prep_grading_dir(assignment_config_path, submission_path)

    result = autograder.submission.run_submission(grading_dir,
            assignment_config_path = assignment_config_path)
    if (result is None):
        return 2

    print(result.report())

    if (args.out_path is not None):
        out_path = os.path.abspath(args.out_path)
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok = True)

        edq.util.json.dump_path(result, out_path, indent = 4)

    if (args.test_submission_path is not None):
        test_submission_path = os.path.abspath(args.test_submission_path)
        if (os.path.isdir(test_submission_path)):
            test_submission_path = os.path.join(test_submission_path, TEST_SUBMISSION_FILENAME)

        os.makedirs(os.path.dirname(test_submission_path), exist_ok = True)

        edq.util.json.dump_path(result.to_test_submission(), test_submission_path, indent = 4)

    return 0

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(__doc__.strip())

    parser.add_argument('-a', '--assignment',
        action = 'store', type = str, required = False, default = DEFAULT_ASSIGNMENT,
        help = 'The path to a JSON file describing an assignment (default: %(default)s).')

    parser.add_argument('-s', '--submission',
        action = 'store', type = str, required = True,
        help = 'The path to a submission to use for grading.')

    parser.add_argument('-o', '--out-path', dest = 'out_path',
        action = 'store', type = str, required = False, default = None,
        help = 'The path to a output the JSON result.')

    parser.add_argument('-t', '--test-submission-path', dest = 'test_submission_path',
        action = 'store', type = str, required = False, default = None,
        help = 'Create a test submission file at the specified path.'
            + ' If an existing dir is provided,'
            + ' a \'%s\' file will be created inside that dir.' % TEST_SUBMISSION_FILENAME)

    return parser

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
