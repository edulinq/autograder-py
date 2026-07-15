"""
Get all submission attempts made by a user along with all grading information.
"""

import argparse
import os
import sys

import autograder.api.courses.assignments.submissions.fetch.user.attempts
import autograder.cli.common
import autograder.cli.parser
import autograder.util.grading

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.application_config

    found_user, grading_results = autograder.api.courses.assignments.submissions.fetch.user.attempts.send(config, exit_on_error = True)

    if (not found_user):
        autograder.cli.common.print_no_match('user', config.target_email)
        return 1

    if (grading_results is None):
        raise ValueError("Existing submissions were not provided by API.")

    if (len(grading_results) == 0):
        print("No attempts found.")
        return 0

    assignment = grading_results[0]['info']['assignment-id']
    user = grading_results[0]['info']['user']
    out_dir = os.path.join(config.out_dir, assignment, user)

    for grading_result in grading_results:
        autograder.util.grading.output_grading_result(grading_result, base_dir = out_dir, short_id = True)

    print(f"Wrote {len(grading_results)} attempts to '{out_dir}'.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.submissions.fetch.user.attempts.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
