import argparse
import json
import os
import sys

import autograder.assignment
import autograder.submission
import autograder.utils

def run(args):
    assignment_path = os.path.abspath(args.assignment)
    submission_path = os.path.abspath(args.submission)

    ext = os.path.splitext(assignment_path)[1]
    if (ext in autograder.code.ALLOWED_EXTENSIONS):
        # The assignment is an assignment class.
        assignment_class = autograder.assignment.fetch_assignment(assignment_path)

        assignment_dir = os.path.dirname(assignment_path)
        submission_dir = submission_path
    elif (ext == '.json'):
        temp_dir, assignment_class = autograder.submission.prep_temp_work_dir(assignment_path,
            submission_path, debug = args.debug)

        assignment_dir = temp_dir
        submission_dir = temp_dir
    else:
        print("Unknown assignment extension: '%s'." % (ext))
        return 1

    result = autograder.submission.run_submission(assignment_class, assignment_dir, submission_dir)
    if (result is None):
        return 2

    print(result.report())

    if (args.outpath is not None):
        out_path = os.path.abspath(args.outpath)
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok = True)
        with open(out_path, 'w') as file:
            json.dump(result.to_dict(), file, indent = 4)

    return 0

def _load_args():
    parser = argparse.ArgumentParser(description =
        'Grade an assignment with the given assignment and submission.' +
        ' If the provided assignment has the ".json" extension,' +
        ' then it is assumed to be an assignment config and the assignment/submission' +
        ' files will be copied to a temp working directory before grading.' +
        ' If the providd assignment has a Python code extension, then no files will be' +
        ' copied and grading will take place in the assignment directory.')

    parser.add_argument('-a', '--assignment',
        action = 'store', type = str, required = True,
        help = 'The path to a JSON/Python file containing assignment information/class.')

    parser.add_argument('-s', '--submission',
        action = 'store', type = str, required = True,
        help = 'The path to a submission to use for grading.')

    parser.add_argument('-o', '--outpath',
        action = 'store', type = str, required = False, default = None,
        help = 'The path to a output the JSON result.')

    parser.add_argument('-d', '--debug', dest = 'debug',
        action = 'store_true', default = False,
        help = 'Enable additional output and leave behind grading artifacts (default: %(default)s)')

    return parser.parse_args()

def main():
    return run(_load_args())

if (__name__ == '__main__'):
    sys.exit(main())
