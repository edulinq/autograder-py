"""
The `autograder.cli.server.users` package contains tools to manage autograder server users.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
