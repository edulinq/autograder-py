import os
import typing

import edq.util.dirent
import edq.util.gzip
import edq.util.json

def output_grading_result(result: typing.Dict[str, typing.Any], base_dir: str = '.', short_id: bool = False) -> str:
    """
    Write out an API grading result (model.GradingResult) to a directory inside the given base directory.
    Any existing directory will be removed (and re-created).
    Return the path to the created directory.
    """

    if (short_id):
        out_dir = os.path.join(base_dir, result['info']['short-id'])
    else:
        long_id = result['info']['id']

        # Windows doesn't like colons in filenames.
        if (os.name == 'nt'):
            long_id = long_id.replace(':', '_')

        out_dir = os.path.join(base_dir, long_id)

    edq.util.dirent.remove(out_dir)
    edq.util.dirent.mkdir(out_dir)

    stdout_path = os.path.join(out_dir, 'stdout.txt')
    edq.util.dirent.write_file(stdout_path, result['stdout'])

    stderr_path = os.path.join(out_dir, 'stderr.txt')
    edq.util.dirent.write_file(stderr_path, result['stderr'])

    result_path = os.path.join(out_dir, 'info.json')
    edq.util.json.dump_path(result['info'], result_path, indent = 4)

    grading_input_dir = os.path.join(out_dir, 'input')
    _output_grading_result_dir(grading_input_dir, result['input-files-gzip'])

    grading_output_dir = os.path.join(out_dir, 'output')
    _output_grading_result_dir(grading_output_dir, result['output-files-gzip'])

    return out_dir

def _output_grading_result_dir(out_dir: str, files: typing.Dict[str, str]) -> None:
    """ Write a collection of gzipped (base64) files to a directory. """

    edq.util.dirent.mkdir(out_dir)

    for (relpath, gzip_contents) in files.items():
        path = os.path.join(out_dir, *relpath.split('/'))
        edq.util.dirent.mkdir(os.path.dirname(path))

        contents = edq.util.gzip.uncompress_base64(gzip_contents)
        edq.util.dirent.write_file_bytes(path, contents)
