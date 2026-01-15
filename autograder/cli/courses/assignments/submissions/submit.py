"""
Submit an assignment submission to the autograder.
"""

import argparse
import sys

import edq.util.time

import autograder.api.courses.assignments.submissions.submit
import autograder.cli.parser

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    result, grading_result = autograder.api.courses.assignments.submissions.submit.send(config, post_paths = args.files)

    message = result.get('message', '')
    if ((message is not None) and (message != '')):
        # Replace any timestamps in the message.
        message = edq.util.time.Timestamp.convert_embedded(message, pretty = True)

        print("--- Message from Autograder ---")
        print(message)
        print("-------------------------------")

    if (result['rejected']):
        print("Submission was rejected by the autograder.")
        return 1

    if (not result['grading-success']):
        print("Grading failed.")
        return 2

    if (grading_result is not None):
        print(grading_result.report())

    return 0

def main() -> int:
    """ Get a parser, parse the args, and call run. """

    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get a parser for this operation. """

    parser = autograder.cli.parser.get_parser(
        __doc__.strip(),
        autograder.api.courses.assignments.submissions.submit.API_PARAMS)

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
