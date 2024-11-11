import json
import os

import autograder.util.dirent
import autograder.util.file
import autograder.util.gzip

def output_grading_result(result, base_dir = '.', short_id = False):
    if short_id:
        out_dir = os.path.join(base_dir, result['info']['short-id'])
    else:
        out_dir = os.path.join(base_dir, result['info']['id'])

    if (os.path.exists(out_dir)):
        autograder.util.dirent.remove(out_dir)

    os.makedirs(out_dir, exist_ok = True)

    stdout_path = os.path.join(out_dir, 'stdout.txt')
    autograder.util.file.write(stdout_path, result['stdout'])

    stderr_path = os.path.join(out_dir, 'stderr.txt')
    autograder.util.file.write(stderr_path, result['stderr'])

    result_path = os.path.join(out_dir, 'info.json')
    autograder.util.file.write(result_path, json.dumps(result['info'], indent = 4))

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
