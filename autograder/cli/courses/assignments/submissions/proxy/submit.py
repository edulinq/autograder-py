"""
Proxy submit an assignment submission to the autograder.
"""

import argparse
import sys

import autograder.cli.courses.assignments.submissions.common
import autograder.api.courses.assignments.submissions.proxy.submit
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    api_response, grading_result = autograder.api.courses.assignments.submissions.proxy.submit.send(config, post_paths = args.files)
    return autograder.cli.courses.assignments.submissions.common.display_grading_result(api_response, grading_result,
            include_found_user = True)

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.submissions.proxy.submit.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
