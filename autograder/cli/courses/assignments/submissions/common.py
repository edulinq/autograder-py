import json
import os

import edq.util.dirent

import autograder.util.gzip

def output_grading_result(result, base_dir = '.', short_id = False):
    if short_id:
        out_dir = os.path.join(base_dir, result['info']['short-id'])
    else:
        long_id = result['info']['id']

        # Windows doesn't like colons in filenames.
        if (os.name == 'nt'):
            long_id = long_id.replace(':', '_')

        out_dir = os.path.join(base_dir, long_id)

    if (os.path.exists(out_dir)):
        edq.util.dirent.remove(out_dir)

    os.makedirs(out_dir, exist_ok = True)

    stdout_path = os.path.join(out_dir, 'stdout.txt')
    edq.util.dirent.write_file(stdout_path, result['stdout'])

    stderr_path = os.path.join(out_dir, 'stderr.txt')
    edq.util.dirent.write_file(stderr_path, result['stderr'])

    result_path = os.path.join(out_dir, 'info.json')
    edq.util.dirent.write_file(result_path, json.dumps(result['info'], indent = 4))

    grading_input_dir = os.path.join(out_dir, 'input')
    _output_grading_result_dir(grading_input_dir, result['input-files-gzip'])

    grading_output_dir = os.path.join(out_dir, 'output')
    _output_grading_result_dir(grading_output_dir, result['output-files-gzip'])

def _output_grading_result_dir(out_dir, files):
    os.makedirs(out_dir, exist_ok = True)

    for (relpath, gzip_contents) in files.items():
        path = os.path.join(out_dir, *relpath.split('/'))
        os.makedirs(os.path.dirname(path), exist_ok = True)

        contents = autograder.util.gzip.from_base64(gzip_contents)
        with open(path, 'wb') as file:
            file.write(contents)
