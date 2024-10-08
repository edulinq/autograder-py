import json
import os
import sys

import autograder.api.courses.upsert.zip
import autograder.error
import autograder.util.zip

def run(arguments):
    try:
        zip_path = _prep_zip(arguments.path)
    except autograder.error.AutograderError as ex:
        print(str(ex))
        return 1

    results = autograder.api.courses.upsert.zip.send(arguments, files = [zip_path],
        exit_on_error = True)

    results = results['results']

    error_count = 0
    for result in results:
        success = result['success']
        course_id = result['course-id']

        if (not success):
            error_count += 1

        if (arguments.full_output):
            continue

        if (not success):
            print("Course '%s' not updated." % (course_id))
            print("Message from server: '%s'." % (result.get('message', '')))
        elif (result.get('created', False)):
            print("Course '%s' created." % (course_id))
        else:
            print("Course '%s' updated." % (course_id))

    if (arguments.full_output):
        print(json.dumps(results, indent = 4))

    return error_count

def _prep_zip(path):
    if (not os.path.exists(path)):
        raise autograder.error.AutograderError("Path does not exist: '%s'." % (path))

    if (os.path.isfile(path)):
        extension = os.path.splitext(path)[1]
        if (extension != '.zip'):
            raise autograder.error.AutograderError(
                "Expecting '.zip' extension, found '%s': '%s'." % (extension, path))

        return path

    return autograder.util.zip.archive_dir(path)

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.upsert.zip._get_parser()

    parser.add_argument('--full-output', dest = 'full_output',
        action = 'store_true', default = False,
        help = 'See the full course update output (as JSON) (default: %(default)s).')

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = ('The path to your course material.'
            + ' Either a zip file (with .zip extension)'
            + ' or durectory (that will get zipped)'))

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
