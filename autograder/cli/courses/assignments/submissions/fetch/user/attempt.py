"""
Get a submission along with all grading information.
"""

import argparse
import sys

import autograder.api.courses.assignments.submissions.fetch.user.attempt
import autograder.cli.common
import autograder.cli.parser
import autograder.util.grading

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config_info.application_config

    found_user, found_submission, result = autograder.api.courses.assignments.submissions.fetch.user.attempt.send(config, exit_on_error = True)

    if (not found_user):
        autograder.cli.common.print_no_match('user', config.target_email)
        return 1

    if (not found_submission):
        autograder.cli.common.print_no_match('submission', config.target_submission)
        return 2

    if (result is None):
        raise ValueError("Existing submission was not provided by API.")

    out_path = autograder.util.grading.output_grading_result(result, base_dir = config.out_dir)
    print(f"Submission wrote to '{out_path}'.")

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.submissions.fetch.user.attempt.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
