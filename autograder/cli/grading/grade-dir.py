import argparse
import json
import os
import sys

import autograder.submission

def run(args):
    grader_path = os.path.abspath(args.grader)
    grading_dir = os.path.abspath(args.dir)

    result = autograder.submission.run_submission(grading_dir, grader_path = grader_path)
    if (result is None):
        return 1

    print(result.report())

    if (args.outpath is not None):
        out_path = os.path.abspath(args.outpath)
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok = True)
        with open(out_path, 'w') as file:
            json.dump(result.to_dict(), file, indent = 4)

    return 0

def _get_parser():
    parser = argparse.ArgumentParser(description =
        'Grade a submission given an already prepared grading directory'
        + ' (see autograder.cli.testing.setup-grading-dir)'
        + ' and a grader file.'
        + ' Use autograder.cli.grading.grade if you have not already prepared'
        + ' your grading directory.')

    parser.add_argument('-g', '--grader',
        action = 'store', type = str, required = True,
        help = 'The path to a Python file containing a single assignment class.')

    parser.add_argument('-d', '--dir',
        action = 'store', type = str, required = True,
        help = 'The path to the grading directory.')

    parser.add_argument('-o', '--outpath',
        action = 'store', type = str, required = False, default = None,
        help = 'The path to a output the JSON result.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
