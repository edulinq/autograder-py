import base64
import sys

import autograder.api.common
import autograder.api.ta.fetchsubmission

def run(arguments):
    out_path = arguments.out_path
    if (not out_path.endswith('.zip')):
        out_path += '.zip'

    config_data = autograder.api.common.parse_config(arguments)
    success, result = autograder.api.ta.fetchsubmission.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    if (not result['found-user']):
        print("Could not find user.")
        return 0

    if (not result['found-submission']):
        print("Could not find any submissions for this user/assignment.")
        return 0

    print("Found submission with ID '%s'." % (result['submission-id']))
    print("Writting output to '%s'." % (out_path))

    data = base64.b64decode(result['contents'], validate = True)

    with open(out_path, 'wb') as file:
        file.write(data)

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(description =
            "Get a user's most recent submission directory.")

    parser.add_argument('email', metavar = 'EMAIL',
        action = 'store', type = str,
        help = 'The email of the user to fetch the submission for.')

    parser.add_argument('-o', '--out-path', dest = 'out_path',
        action = 'store', type = str, default = 'submission.zip',
        help = 'Where to write the submission output to (as a zip file).')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
