"""
The `autograder.cli.stats` package contains tools for
managing stats from the autograder server.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
