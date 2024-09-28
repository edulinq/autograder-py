import argparse
import os
import subprocess
import sys

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.join(THIS_DIR, '..')

# Add in the root path.
sys.path.append(ROOT_DIR)

import tests.server.server

def build_api_args(server, additional_arguments = {}):
    if (isinstance(additional_arguments, argparse.Namespace)):
        additional_arguments = vars(additional_arguments)

    arguments = tests.server.server.INITIAL_BASE_ARGUMENTS.copy()
    for key, value in additional_arguments.items():
        if ((value is not None) or (value)):
            arguments[key] = value

    arguments['server'] = server.get_address()

    return arguments

def run(args, cwd = '.', raise_on_error = True, print_output = False):
    try:
        subprocess.run(args, cwd = cwd, check = raise_on_error, capture_output = (not print_output))
    except subprocess.CalledProcessError as ex:
        print("--- stdout ---")
        print(ex.stdout)
        print("--------------")
        print("--- stderr ---")
        print(ex.stderr)
        print("--------------")

        raise ex

def run_in_background(args, cwd = '.'):
    return subprocess.Popen(args, cwd = cwd)
