import sys

import autograder.api.common
import autograder.api.canvas.uploadscores

KEY_COUNT = 'count'

def run(arguments):
    config_data = autograder.api.common.parse_config(arguments)
    config_data['scores'] = _load_scores(arguments.path)

    success, result = autograder.api.canvas.uploadscores.send(arguments.server, config_data)

    if (not success):
        print(result)
        return 1

    print("Upload complete.")
    print("    Grades Uploaded: %d" % (result['count']))
    print("    Errors: %d" % (result['error-count']))

    check_lists = [
        ['Unrecognized Users', 'unrecognized-users'],
        ['Users without Canvas IDs', 'no-canvas-id-users'],
        ['Malformed Scores', 'bad-scores'],
    ]

    for (name, key) in check_lists:
        print("        %s: %d" % (name, len(result[key])))
        for value in result[key]:
            print("            %s" % (value))

    return 0

def _load_scores(path):
    scores = []

    with open(path, 'r') as file:
        lineno = 0
        for line in file:
            lineno += 1

            line = line.strip()
            if (line == ""):
                continue

            parts = line.split("\t")
            if (len(parts) != 2):
                raise ValueError(
                    "File ('%s') line (%d) has the incorrect number of values." % (path, lineno)
                    + " Expecting 2, found %d." % (len(parts)))

            scores.append(parts)

    return scores

def _get_parser():
    parser = autograder.api.common.get_argument_parser(
        description = 'Upload scores (from a TSV file) to Canvas for the specified assignment.',
        include_assignment = False)

    parser.add_argument('assignment-id', metavar = 'ASSIGNMENT_CANVAS_ID',
        action = 'store', type = str,
        help = 'The Canvas ID of the assignment to upload grades for.')

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file with two columns: email and score.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
