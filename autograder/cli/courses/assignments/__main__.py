"""
The `autograder.cli.courses.assignments` package contains tools to access and
manage assignment information.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
