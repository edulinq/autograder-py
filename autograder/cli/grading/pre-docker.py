# pylint: disable=invalid-name

"""
Take any necessary steps before performing a standard docker-based grading.
This script is used as part of the standard docker grading procedure for Python.
"""

import argparse
import os
import sys

import edq.util.dirent
import edq.util.json

import autograder.fileop
import autograder.submission

DEFAULT_BASE_DIR: str = os.path.join('/', 'autograder')

DEFAULT_CONFIG_PATH: str = os.path.join(DEFAULT_BASE_DIR, 'config.json')

DEFAULT_INPUT_DIR: str = os.path.join(DEFAULT_BASE_DIR, 'input')
DEFAULT_OUTPUT_DIR: str = os.path.join(DEFAULT_BASE_DIR, 'output')
DEFAULT_WORK_DIR: str = os.path.join(DEFAULT_BASE_DIR, 'work')

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    if (not os.path.exists(args.config)):
        # No config, there's nothing to do.
        return 0

    config = edq.util.json.load_path(args.config)

    edq.util.dirent.mkdir(args.basedir)
    edq.util.dirent.mkdir(args.inputdir)
    edq.util.dirent.mkdir(args.outputdir)
    edq.util.dirent.mkdir(args.workdir)

    # Do post-submission file operations.
    # There are no pre-sub file ops and Docker has already copied over the submission files
    # into the input directory.
    operations = config.get(autograder.submission.CONFIG_KEY_POST_SUB_OPS, [])
    autograder.fileop.exec_file_operations(operations, args.basedir)

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    args, _ = _get_parser().parse_known_args()
    return run_cli(args)

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = argparse.ArgumentParser(description = __doc__.strip())

    parser.add_argument('-c', '--config',
        action = 'store', type = str, default = DEFAULT_CONFIG_PATH,
        help = 'The path to a JSON file describing grading configurations (default: %(default)s).')

    parser.add_argument('-bd', '--basedir',
        action = 'store', type = str, default = DEFAULT_BASE_DIR,
        help = 'The path to the base dir (where file operations are run) (default: %(default)s).')

    parser.add_argument('-id', '--inputdir',
        action = 'store', type = str, default = DEFAULT_INPUT_DIR,
        help = 'The path to the grading input directory (default: %(default)s).')

    parser.add_argument('-od', '--outputdir',
        action = 'store', type = str, default = DEFAULT_OUTPUT_DIR,
        help = 'The path to the grading output directory (default: %(default)s).')

    parser.add_argument('-wd', '--workdir',
        action = 'store', type = str, default = DEFAULT_WORK_DIR,
        help = 'The path to the grading work directory (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
