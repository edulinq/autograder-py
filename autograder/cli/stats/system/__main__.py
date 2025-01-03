"""
The `autograder.cli.stats.system` package contains tools for
managing system-level stats from the autograder server.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
