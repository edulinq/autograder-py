"""
Commands to make, query, and manage submissions to the autograder.
"""

import os
import sys

import autograder.util.cli

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.join(THIS_DIR, '..', '..', '..')

def run():
    relpath = os.path.relpath(THIS_DIR, start = ROOT_DIR)
    package = '.'.join(relpath.split(os.sep))

    print(__doc__.strip())
    autograder.util.cli.list_dir(THIS_DIR, package)
    return 0

def main():
    return run()

if (__name__ == '__main__'):
    sys.exit(main())
