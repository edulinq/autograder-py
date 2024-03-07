"""
The `autograder.cli.admin` package contains tools for
administering an autograder course/server.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
