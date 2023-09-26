import argparse
import os
import sys

import autograder.submission

def run(args):
    assignment_config_path = os.path.abspath(args.assignment)
    submission_path = os.path.abspath(args.submission)
    base_dir = os.path.abspath(args.dir)

    input_dir, output_dir, work_dir = autograder.submission.prep_grading_dir(
        assignment_config_path, base_dir, submission_path,
        skip_static = args.skip_static)

    return 0

def _get_parser():
    parser = argparse.ArgumentParser(description =
        'Setup a directory as if it is being graded.')

    parser.add_argument('-a', '--assignment',
        action = 'store', type = str, required = True,
        help = 'The path to a JSON file describing an assignment.')

    parser.add_argument('-s', '--submission',
        action = 'store', type = str, required = True,
        help = 'The path to an input submission.')

    parser.add_argument('--dir',
        action = 'store', type = str, required = True,
        help = 'The target directory to prepare.')

    parser.add_argument('-ss', '--skip-static', dest = 'skip_static',
        action = 'store_true', default = False,
        help = 'Skip the static portion of the setup (copy and ops) (default: %(default)s)')

    parser.add_argument('-d', '--debug', dest = 'debug',
        action = 'store_true', default = False,
        help = 'Enable additional output and leave behind grading artifacts (default: %(default)s)')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
