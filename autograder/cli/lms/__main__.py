"""
The `autograder.cli.lms` package contains tools to bridge
Learning Management Systems (LMSs) like Canvas and the autograder.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
