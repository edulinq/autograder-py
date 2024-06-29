"""
The `autograder.cli.lms` package contains tools to bridge
Learning Management Systems (LMSs) like Canvas and the autograder.
"""

import sys

import autograder.util.cli

def main():
    autograder.util.cli.auto_list()
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
