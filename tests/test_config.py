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
            rel_global_config_dir_path = ["global"]
            rel_config_dir_path = ["config"]
            rel_ancestor_config_dir_path = ["code"]
            rel_test_assignment_dir_path= rel_ancestor_config_dir_path + ["course101", "hw1"]

            test_cases = [
                ((rel_ancestor_config_dir_path, "autograder.json"), "<default config file>", rel_ancestor_config_dir_path + ["autograder.json"], False, False),
                ((rel_test_assignment_dir_path, "config.json"), "<default config file>", rel_test_assignment_dir_path + ["config.json"], False, False),
                ((rel_test_assignment_dir_path, "autograder.json"), "<default config file>", rel_test_assignment_dir_path + ["autograder.json"], False, False),
                ((None), "<user config file>", rel_global_config_dir_path + ["autograder.json"], False, True),
                ((None), "<cli config file>", rel_config_dir_path + ["test-config.json"], True, False),
                ((rel_test_assignment_dir_path, "autograder.json"), "<cli config file>", rel_config_dir_path + ["test-config.json"], True, True)
            ]

            for test_case in test_cases:
                temp_dir = autograder.util.dirent.get_temp_path('autograder-test-config-')
                (local_config), config_type, rel_expected_config_path, cli_config_exists, global_config_exists = test_case

                rel_expected_config_path = [temp_dir]+ rel_expected_config_path
                expected_config_path = os.path.join(*rel_expected_config_path)

                global_config_dir_path = [temp_dir] + rel_global_config_dir_path
                abs_global_config_dir_path = os.path.join(*global_config_dir_path)

                config_dir_path = [temp_dir] + rel_config_dir_path
                abs_config_dir_path= os.path.join(*config_dir_path)

                ancestor_config_dir_path = [temp_dir] + rel_ancestor_config_dir_path
                abs_ancestor_config_dir_path= os.path.join(*ancestor_config_dir_path)

                test_assignment_dir_path= [temp_dir] + rel_test_assignment_dir_path
                abs_test_assignment_dir_path = os.path.join(*test_assignment_dir_path)

                autograder.util.dir.mkdir(temp_dir)
                autograder.util.dir.mkdir(abs_global_config_dir_path)
                autograder.util.dir.mkdir(abs_config_dir_path)
                autograder.util.dir.mkdir(abs_ancestor_config_dir_path)
                autograder.util.dir.mkdir(abs_test_assignment_dir_path)

                if local_config is not None:
                    path_to_local_config, name_config = local_config

                    path_to_local_config = [temp_dir] + path_to_local_config
                    abs_path_to_local_config = os.path.join(*path_to_local_config)
                    write_config(EXPECTED_CONFIG, abs_path_to_local_config, name_config)

                config_paths = None
                if cli_config_exists:
                    cli_config = write_config(EXPECTED_CONFIG, abs_config_dir_path, "test-config.json")
                    config_paths = [cli_config]

                global_file_path = abs_global_config_dir_path
                if global_config_exists:
                    global_file_path = write_config(EXPECTED_CONFIG, abs_global_config_dir_path, "autograder.json")

                expected_source = {
                    "course": f"{config_type}:: {expected_config_path}",
                    "assignment": f"{config_type}:: {expected_config_path}",
                    "server": f"{config_type}:: {expected_config_path}",
                    "user": f"{config_type}:: {expected_config_path}",
                    "pass": f"{config_type}:: {expected_config_path}"
                }

                os.chdir(abs_test_assignment_dir_path)
                actual_configs, actual_sources = autograder.api.config.get_tiered_config(
                    argparse.Namespace(config_paths = config_paths),
                    show_sources = True,
                    global_config_path = global_file_path
                )

                self.assertEqual(actual_configs, EXPECTED_CONFIG)
                self.assertEqual(actual_sources, expected_source)
            os.chdir(cwd)

