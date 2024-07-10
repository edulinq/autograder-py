"""
The `autograder.cli.submissions` package contains tools to
make, query, and manage submissions to the autograder.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
