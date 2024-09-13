"""
The `autograder.cli.courses.admin` package contains tools for
administering an autograder course.
"""

import sys

import autograder.util.cli

def main():
    return autograder.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
