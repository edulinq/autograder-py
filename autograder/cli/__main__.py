"""
Look in the autograder.cli package for modules that look like CLI tools
(has a _get_parser() method that returns an argparse parser)
and list them.
"""

import os
import sys

import autograder.code

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def run():
    print("The autograder CLI package contains several tools for interacting with the autograder.")
    print("The following is a non-exhaustive list of CLI tools.")
    print("Invoke each command with the `--help` option for more details.")

    for dirent in sorted(os.listdir(THIS_DIR)):
        path = os.path.join(THIS_DIR, dirent)
        cmd = 'autograder.cli.' + os.path.splitext(dirent)[0]

        if (dirent.startswith('__')):
            continue

        try:
            module = autograder.code.import_path(path)
        except Exception:
            continue

        if ('_get_parser' not in dir(module)):
            continue

        parser = module._get_parser()
        parser.prog = 'python3 -m ' + cmd

        print()
        print(cmd)
        print(parser.description)
        parser.print_usage()

    return 0

def main():
    return run()

if (__name__ == '__main__'):
    sys.exit(main())
