"""
The `autograder.cli.courses` package contains tools to manage autograder courses.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
