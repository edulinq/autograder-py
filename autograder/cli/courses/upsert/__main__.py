"""
The `autograder.cli.courses.upsert` package contains tools for upserting an autograder course.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
