import os

import autograder.util.dirent

def get_temp_dir(**kwargs):
    path = autograder.util.dirent.get_temp_path(**kwargs)
    mkdir(path)
    return path

def mkdir(path):
    os.makedirs(path, exist_ok = True)
