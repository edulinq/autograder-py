"""
General utility commands.
"""

import os
import sys

import autograder.util.cli

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def run():
    print(__doc__.strip())
    autograder.util.cli.list_dir(THIS_DIR, 'autograder.cli.util')
    return 0

def main():
    return run()

if (__name__ == '__main__'):
    sys.exit(main())
