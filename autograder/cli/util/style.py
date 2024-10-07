import argparse
import sys

import autograder.style

def run(args):
    count, total_lines = autograder.style.check_paths(args.paths, ignore_paths = args.ignore_paths)
    print("Found %d style errors." % (count))

    if (count > 0):
        for (path, lines) in total_lines:
            print("\nStyle Errors for '%s':" % (path))
            print('---')
            print("\n".join(lines))
            print("---\n")

    return count

def _get_parser():
    parser = argparse.ArgumentParser(description =
        "Check the style of all '.py' and '.ipynb' files in the paths specified (recursively).")

    parser.add_argument('--ignore', dest = 'ignore_paths',
        type = str, action = 'append', default = [],
        help = 'Paths to ignore (may be specified mulitiple times).')

    parser.add_argument('paths', metavar = 'path',
        type = str, nargs = '+',
        help = 'A path to check for style.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
