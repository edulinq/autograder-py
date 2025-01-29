#!/usr/bin/env python3

import json
import os
import sys

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.join(THIS_DIR, '..')

# Add in the root path.
sys.path.append(ROOT_DIR)

import tests.server.server

def main():
    responses, _, _ = tests.server.server.build_api_responses()
    print(json.dumps(responses, indent = 4))
    return 0

if __name__ == '__main__':
    sys.exit(main())
