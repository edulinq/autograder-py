import os
import sys

import autograder.api.courses.upsert.zip
import autograder.cli.courses.upsert.common
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

    return autograder.cli.courses.upsert.common.handle_results(results,
        arguments.full_output)

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

    autograder.cli.courses.upsert.common.add_full_output_argument(parser)

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = ('The path to your course material.'
            + ' Either a zip file (with .zip extension)'
            + ' or durectory (that will get zipped)'))

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
