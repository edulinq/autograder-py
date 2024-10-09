import sys

import autograder.api.courses.upsert.filespec
import autograder.cli.courses.upsert.common

def run(arguments):
    arguments = vars(arguments)

    filespec = _build_filespec(arguments)
    arguments['filespec'] = filespec

    results = autograder.api.courses.upsert.filespec.send(arguments, exit_on_error = True)

    return autograder.cli.courses.upsert.common.handle_results(results,
        arguments['full_output'])

def _build_filespec(arguments):
    filespec = {
        'type': arguments['type'],
        'path': arguments['path'],
    }

    for key in ['reference', 'username', 'token']:
        value = arguments.get(key, None)
        if (value is None):
            continue

        filespec[key] = value

    return filespec

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.upsert.filespec._get_parser()

    autograder.cli.courses.upsert.common.add_full_output_argument(parser)

    parser.add_argument('--type', dest = 'type',
        action = 'store', type = str, required = True,
        choices = ['git', 'url'],
        help = 'The type of filespec.')

    parser.add_argument('--path', dest = 'path',
        action = 'store', type = str, required = True,
        help = 'The path the filespec points to.')

    parser.add_argument('--reference', dest = 'reference',
        action = 'store', type = str, default = None,
        help = 'The reference (often git commit/branch) of the filespec.')

    parser.add_argument('--username', dest = 'username',
        action = 'store', type = str, default = None,
        help = 'The username for filespec authentication.')

    parser.add_argument('--token', dest = 'token',
        action = 'store', type = str, default = None,
        help = 'The token for filespec authentication.')

    # Note that dest is not used for course upserting (the name of the dirs do not matter).

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
