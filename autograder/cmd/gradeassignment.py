import argparse
import json
import os
import sys

import autograder.submission

DEFAULT_ASSIGNMENT = 'assignment.json'

def run(args):
    assignment_path = os.path.abspath(args.assignment)
    submission_path = os.path.abspath(args.submission)

    dirs, assignment_class = autograder.submission.prep_temp_grading_dir(assignment_path,
        submission_path, debug = args.debug)

    input_dir, output_dir, work_dir = dirs

    result = autograder.submission.run_submission(assignment_class, input_dir, output_dir, work_dir)
    if (result is None):
        return 2

    print(result.report())

    if (args.outpath is not None):
        out_path = os.path.abspath(args.outpath)
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok = True)
        with open(out_path, 'w') as file:
            json.dump(result.to_dict(), file, indent = 4)

    return 0

def _get_parser():
    parser = argparse.ArgumentParser(description =
        'Grade an assignment (specified by an assignment JSON file) using the given submission.')

    parser.add_argument('-a', '--assignment',
        action = 'store', type = str, required = False, default = DEFAULT_ASSIGNMENT,
        help = 'The path to a JSON file describing an assignment (default: %(default)s).')

    parser.add_argument('-s', '--submission',
        action = 'store', type = str, required = True,
        help = 'The path to a submission to use for grading.')

    parser.add_argument('-o', '--outpath',
        action = 'store', type = str, required = False, default = None,
        help = 'The path to a output the JSON result.')

    parser.add_argument('-d', '--debug', dest = 'debug',
        action = 'store_true', default = False,
        help = 'Enable additional output and leave behind artifacts (default: %(default)s).')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
