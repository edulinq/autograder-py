"""
Look in a package for modules that look like CLI tools
(has a _get_parser() method that returns an argparse parser)
and list them.
"""

import os

import autograder.code

def handle_file(path, cmd):
    try:
        module = autograder.code.import_path(path)
    except Exception:
        return

    if ('_get_parser' not in dir(module)):
        return

    parser = module._get_parser()
    parser.prog = 'python3 -m ' + cmd

    print()
    print(cmd)
    print(parser.description)
    parser.print_usage()

def handle_dir(path, cmd):
    try:
        module = autograder.code.import_path(os.path.join(path, '__main__.py'))
    except Exception:
        return

    description = module.__doc__.strip()

    print()
    print(cmd + '.*')
    print(description)
    print("See `python3 -m %s` for more information." % (cmd))

def list_dir(base_dir, command_prefix):
    for dirent in sorted(os.listdir(base_dir)):
        path = os.path.join(base_dir, dirent)
        cmd = command_prefix + '.' + os.path.splitext(dirent)[0]

        if (dirent.startswith('__')):
            continue

        if (os.path.isfile(path)):
            handle_file(path, cmd)
        else:
            handle_dir(path, cmd)
