import os
import sys

import autograder.api.submissions.fetchattempts
import autograder.cli.submissions.common

def run(arguments):
    result = autograder.api.submissions.fetchattempts.send(arguments, exit_on_error = True)

    if (not result['found-user']):
        print("No matching user found.")
        return 1

    if (len(result['grading-results']) == 0):
        print("No attempts found.")
        return 2

    assignment = result['grading-results'][0]['info']['assignment-id']
    user = result['grading-results'][0]['info']['user']
    out_dir = os.path.join(arguments.out_dir, assignment, user)

    for grading_result in result['grading-results']:
        autograder.cli.submissions.common.output_grading_result(grading_result, out_dir, True)

    print("Wrote %d attempts to '%s'." % (len(result['grading-results']), out_dir))

    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.submissions.fetchattempts._get_parser()

    parser.add_argument('-o', '--out-dir', dest = 'out_dir',
        action = 'store', type = str, default = '.',
        help = ('Where to create a new directory that will contain submission attempts.'
            + ' An existing subdirectory will be removed.'
            + ' Defaults to the current directory.'))

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
