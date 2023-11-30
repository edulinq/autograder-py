import ast
import sys

import autograder.api.lms.uploadscores

def run(arguments):
    arguments = vars(arguments)
    arguments['scores'] = _load_scores(arguments['path'])

    result = autograder.api.lms.uploadscores.send(arguments, exit_on_error = True)

    print("Upload complete.")
    print("    Grades Uploaded: %d" % (result['count']))
    print("    Errors: %d" % (result['error-count']))

    check_lists = [
        ['Unrecognized Users', 'unrecognized-users'],
        ['Users without LMS IDs', 'no-lms-id-users'],
    ]

    for (name, key) in check_lists:
        if ((key not in result) or (result[key] is None)):
            continue

        print("        %s: %d" % (name, len(result[key])))
        for value in result[key]:
            print("            Row %d -- %s" % (value['row'], value['entry']))

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

            try:
                parts[1] = ast.literal_eval(parts[1])
            except Exception as ex:
                raise ValueError(
                    "File ('%s') line (%d) has a score that cannot be" % (path, lineno)
                    + " converted to a number: '%s'." % (line)) from ex

            scores.append({
                'email': parts[0],
                'score': parts[1],
            })

    return scores

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.lms.uploadscores._get_parser()

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file with two columns: email and score.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
