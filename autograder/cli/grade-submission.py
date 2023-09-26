import argparse
import json
import os
import sys

import autograder.assignment
import autograder.submission
import autograder.utils

def run(args):
    grader_path = os.path.abspath(args.grader)
    work_dir = os.path.abspath(args.workdir)

    input_dir = args.inputdir
    if (input_dir is None):
        input_dir = work_dir
    input_dir = os.path.abspath(input_dir)

    output_dir = args.outputdir
    if (output_dir is None):
        output_dir = work_dir
    output_dir = os.path.abspath(output_dir)

    assignment_class = autograder.assignment.fetch_assignment(grader_path)

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
        'Grade a submission given an already prepared working (submission) directory'
        + ' and a grader file.'
        + ' Use autograder.cli.grade-assignment if you have not already prepared'
        + ' your work directory.')

    parser.add_argument('-g', '--grader',
        action = 'store', type = str, required = True,
        help = 'The path to a Python file containing a single assignment class.')

    parser.add_argument('-id', '--inputdir',
        action = 'store', type = str, required = False, default = None,
        help = 'The path to the submission\'s input directory (defaults to the work directory).')

    parser.add_argument('-od', '--outputdir',
        action = 'store', type = str, required = False, default = None,
        help = 'The path to the submission\'s output directory (defaults to the work directory).')

    parser.add_argument('-wd', '--workdir',
        action = 'store', type = str, required = True,
        help = 'The path to a submission to use for grading.')

    parser.add_argument('-o', '--outpath',
        action = 'store', type = str, required = False, default = None,
        help = 'The path to a output the JSON result.')

    parser.add_argument('-d', '--debug', dest = 'debug',
        action = 'store_true', default = False,
        help = 'Enable additional output and leave behind artifacts (default: %(default)s)')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
