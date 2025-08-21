"""
The `autograder.cli.config` package contains tools
for viewing and changing autograder configurations.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
