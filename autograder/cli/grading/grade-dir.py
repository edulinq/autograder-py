# pylint: disable=invalid-name

"""
Grade a submission given an already prepared grading directory (see autograder.cli.testing.setup-grading-dir) and a grader file.
Use autograder.cli.grading.grade if you have not already prepared your grading directory.
"""

import argparse
import os
import sys

import edq.util.dirent
import edq.util.json

import autograder.submission

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    grader_path = os.path.abspath(args.grader)
    grading_dir = os.path.abspath(args.dir)

    result = autograder.submission.run_submission(grading_dir, grader_path = grader_path)
    if (result is None):
        return 1

    print(result.report())

    if (args.outpath is not None):
        out_path = os.path.abspath(args.outpath)
        edq.util.dirent.mkdir(os.path.dirname(os.path.abspath(out_path)))
        edq.util.json.dump_path(result.to_dict(), out_path, indent = 4)

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    args, _ = _get_parser().parse_known_args()
    return run_cli(args)

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = argparse.ArgumentParser(description = __doc__.strip())

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

if (__name__ == '__main__'):
    sys.exit(main())
