"""
The `autograder.cli.system` package contains tools for
interacting with the system/server running the autograder.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
