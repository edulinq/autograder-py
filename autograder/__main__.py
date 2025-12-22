"""
The `autograder` package is the root of the Python interface to the Lynx autograder.
To invoke the CLI, use the `autograder.cli` or `autograder.run` packages.
Each package can be invoked to list the tools (or subpackages) it contains.
Each tool includes a help prompt that accessed with the `-h`/`--help` flag.
"""

import sys

import edq.util.cli

def main() -> int:
    """ List this CLI dir. """

    return edq.util.cli.main()

if (__name__ == '__main__'):
    sys.exit(main())
