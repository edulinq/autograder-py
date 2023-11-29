import argparse
import json
import os
import sys

import autograder.submission

DEFAULT_ASSIGNMENT = 'assignment.json'
TEST_SUBMISSION_FILENAME = 'test-submission.json'

def run(args):
    assignment_path = os.path.abspath(args.assignment)
    submission_path = os.path.abspath(args.submission)

    grading_dir = autograder.submission.prep_grading_dir(assignment_path,
        submission_path, debug = args.debug)

    result = autograder.submission.run_submission(grading_dir)
    if (result is None):
        return 2

    print(result.report())

    if (args.out_path is not None):
        out_path = os.path.abspath(args.out_path)
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok = True)

        with open(out_path, 'w') as file:
            json.dump(result.to_dict(), file, indent = 4)

    if (args.test_submission_path is not None):
        test_submission_path = os.path.abspath(args.test_submission_path)
        if (os.path.isdir(test_submission_path)):
            test_submission_path = os.path.join(test_submission_path, TEST_SUBMISSION_FILENAME)

        os.makedirs(os.path.dirname(test_submission_path), exist_ok = True)

        with open(test_submission_path, 'w') as file:
            json.dump(result.to_test_submission(), file, indent = 4)

    return 0

def _create_test_submission(result):
    result = result.to_dict()

def _get_parser():
    parser = argparse.ArgumentParser(description =
        'Grade an assignment (specified by an assignment JSON file) with the given submission.')

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

    parser.add_argument('-d', '--debug', dest = 'debug',
        action = 'store_true', default = False,
        help = 'Enable additional output and leave behind artifacts (default: %(default)s).')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
