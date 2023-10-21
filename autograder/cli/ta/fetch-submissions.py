import base64
import sys

import autograder.api.common
import autograder.api.ta.fetchsubmissions

def run(arguments):
    out_path = arguments.out_path
    if (not out_path.endswith('.zip')):
        out_path += '.zip'

    config_data = autograder.api.common.parse_config(arguments)
    success, result = autograder.api.ta.fetchsubmissions.send(config_data.get("server"),
            config_data)

    if (not success):
        print(result)
        return 1

    if (len(result['submission-ids']) == 0):
        print("Could not find any submissions for this assignment.")
        return 0

    print("Found %d submissions." % (len(result['submission-ids'])))
    print("Writting output to '%s'." % (out_path))

    data = base64.b64decode(result['contents'], validate = True)

    with open(out_path, 'wb') as file:
        file.write(data)

    return 0

def _get_parser():
    parser = autograder.api.common.get_argument_parser(description =
            "Get all user's most recent submission directory for an assignment.")

    parser.add_argument('-o', '--out-path', dest = 'out_path',
        action = 'store', type = str, default = 'submissions.zip',
        help = 'Where to write the submission output to (as a zip file) (default: %(default)s).')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
