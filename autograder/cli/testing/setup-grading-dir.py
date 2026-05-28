# pylint: disable=invalid-name

"""
Setup a directory as if it is being graded.
This is useful for seeing what the autograder will see right before grading begins.
"""

import argparse
import os
import sys

import autograder.cli.parser
import autograder.submission

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    assignment_config_path = os.path.abspath(args.assignment)
    submission_path = os.path.abspath(args.submission)

    grading_dir = autograder.submission.prep_grading_dir(
        assignment_config_path, submission_path,
        grading_dir = args.out_dir,
        skip_static = args.skip_static,
    )

    print(f"Prepared grading directory: '{grading_dir}'.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    parser = autograder.cli.parser.get_parser(__doc__.strip())

    parser.add_argument('-a', '--assignment',
        action = 'store', type = str, required = True,
        help = 'The path to an assignment JSON file.')

    parser.add_argument('-s', '--submission',
        action = 'store', type = str, required = True,
        help = 'The path to an input submission.')

    parser.add_argument('-o', '--out-dir', dest = 'out_dir',
        action = 'store', type = str, default = None,
        help = 'The base output directory. Will be a temp directory if not specified.')

    parser.add_argument('-ss', '--skip-static', dest = 'skip_static',
        action = 'store_true', default = False,
        help = 'Skip the static portion of the setup (copy and ops) (default: %(default)s)')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
