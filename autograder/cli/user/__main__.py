"""
Commands to manage autograder users.
"""

import os
import sys

import autograder.util.cli

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def run():
    print("The autograder CLI package contains several tools for interacting with the autograder.")
    print("The following is a non-exhaustive list of CLI tools.")
    print("Invoke each command with the `--help` option for more details.")

    autograder.util.cli.list_dir(THIS_DIR, 'autograder.cli.user')
    return 0

def main():
    return run()

if (__name__ == '__main__'):
    sys.exit(main())
