"""
Check the style of all '.py' and '.ipynb' files in the paths specified (recursively).
"""

import argparse
import sys

import autograder.cli.parser
import autograder.style

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    count, total_lines = autograder.style.check_paths(args.paths,
            ignore_paths = args.ignore_paths, ignore_patterns = args.ignore_patterns)
    print(f"Found {count} style errors.")

    if (count > 0):
        for (path, lines) in total_lines:
            print(f"\nStyle Errors for '{path}':")
            print('---')
            print("\n".join(lines))
            print("---\n")

    return count

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    parser = autograder.cli.parser.get_parser(__doc__.strip())

    parser.add_argument('paths', metavar = 'path',
        type = str, nargs = '+',
        help = 'A path to check for style.')

    parser.add_argument('--ignore-path', dest = 'ignore_paths',
        type = str, action = 'append', default = [],
        help = 'Paths to ignore (may be specified multiple times).')

    parser.add_argument('--ignore-pattern', dest = 'ignore_patterns',
        type = str, action = 'append', default = [],
        help = 'Regular expressions to ignore (may be specified multiple times).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
