import argparse
import json
import os
import sys

import autograder.submission

DEFAULT_BASE_DIR = os.path.join('/', 'autograder')

DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_BASE_DIR, 'config.json')

DEFAULT_INPUT_DIR = os.path.join(DEFAULT_BASE_DIR, 'input')
DEFAULT_OUTPUT_DIR = os.path.join(DEFAULT_BASE_DIR, 'output')
DEFAULT_WORK_DIR = os.path.join(DEFAULT_BASE_DIR, 'work')

def run(args):
    if (not os.path.exists(args.config)):
        # No config, there's nothing to do.
        return 0

    with open(args.config, 'r') as file:
        config = json.load(file)

    os.makedirs(args.basedir, exist_ok = True)
    os.makedirs(args.inputdir, exist_ok = True)
    os.makedirs(args.outputdir, exist_ok = True)
    os.makedirs(args.workdir, exist_ok = True)

    # Do post-submission file operations.
    # There are no pre-sub file ops and Docker has already copied over the submission files
    # into the input directory.
    for file_operation in config.get(autograder.submission.CONFIG_KEY_POST_SUB_OPS, []):
        autograder.submission.do_file_operation(file_operation, args.basedir)

    return 0

def _get_parser():
    parser = argparse.ArgumentParser(description =
        'Take any necessary steps before performing a standard docker-based grading.'
        + ' This script is used as part of the standard docker grading procedure for Python.')

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

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
