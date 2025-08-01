import argparse
import json
import os
import unittest

import autograder.api.config
import autograder.util.dir
import autograder.util.dirent

EXPECTED_CONFIG = { 
    "course": "course101",
    "assignment": "hw1",
    "server": "http://testserver.edu",
    "user": "course-student@test.edulinq.org",
    "pass": "course-student"
}

def write_config(data, config_path, config_name):
    config_file = os.path.join(config_path, config_name)
    with open(config_file, 'w') as file:
        json.dump(data, file, indent = 4)

    return config_file

class TestConfig(unittest.TestCase):
    def test_base(self):
            cwd = os.getcwd()
            temp_dir = autograder.util.dirent.get_temp_path('autograder-test-config-')
            global_config_dir_path = os.path.join(temp_dir, "global")
            config_dir_path = os.path.join(temp_dir, "config")
            ancestor_config_dir_path = os.path.join(temp_dir, "code")
            test_assignment_dir_path= os.path.join(ancestor_config_dir_path, "course101", "hw1")

            test_cases = [
                ((ancestor_config_dir_path, "autograder.json"), "<default config file>", os.path.join(ancestor_config_dir_path, "autograder.json"), False, False),
                ((test_assignment_dir_path, "config.json"), "<default config file>", os.path.join(test_assignment_dir_path, "config.json"), False, False),
                ((test_assignment_dir_path, "autograder.json"), "<default config file>", os.path.join(test_assignment_dir_path, "autograder.json"), False, False),
                ((None), "<user config file>", os.path.join(global_config_dir_path, "autograder.json"),False, True),
                ((None), "<cli config file>", os.path.join(config_dir_path, "test-config.json"), True, False),
                ((test_assignment_dir_path, "autograder.json"), "<cli config file>", os.path.join(config_dir_path, "test-config.json"), True, True)
            ]

            for test_case in test_cases:
                (local_config), config_type, expected_config_path, cli_config_exists, global_config_exists = test_case

                autograder.util.dir.mkdir(temp_dir)
                autograder.util.dir.mkdir(global_config_dir_path)
                autograder.util.dir.mkdir(config_dir_path)
                autograder.util.dir.mkdir(ancestor_config_dir_path)
                autograder.util.dir.mkdir(test_assignment_dir_path)

                os.chdir(test_assignment_dir_path)

                if local_config is not None:
                    path_to_local_config, name_config = local_config
                    write_config(EXPECTED_CONFIG, path_to_local_config, name_config)

                config_paths = None
                if cli_config_exists:
                    cli_config = write_config(EXPECTED_CONFIG, config_dir_path, "test-config.json")
                    config_paths = [cli_config]

                global_file_path = global_config_dir_path
                if global_config_exists:
                    global_file_path = write_config(EXPECTED_CONFIG, global_config_dir_path, "autograder.json")

                expected_source = {
                    "course": f"{config_type}:: {expected_config_path}",
                    "assignment": f"{config_type}:: {expected_config_path}",
                    "server": f"{config_type}:: {expected_config_path}",
                    "user": f"{config_type}:: {expected_config_path}",
                    "pass": f"{config_type}:: {expected_config_path}"
                }

                actual_configs, actual_sources = autograder.api.config.get_tiered_config(
                    argparse.Namespace(config_paths = config_paths),
                    show_sources = True,
                    global_config_path = global_file_path
                )

                self.assertEqual(actual_configs, EXPECTED_CONFIG)
                self.assertEqual(actual_sources, expected_source)

                autograder.util.dirent.remove(temp_dir)
            os.chdir(cwd)

