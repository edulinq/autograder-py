import argparse
import json
import os
import unittest

import autograder.api.config
import autograder.util.dir
import autograder.util.dirent

DEFAULT_CONFIG = {
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

def get_config_with_abs_path(data, cwd):
    result = {}
    for config, (type_config, rel_path) in data.items():
        abs_path = [cwd] + rel_path
        result.update({config: f"{type_config} {os.path.join(*abs_path)}"})
    return result

     
class TestConfig(unittest.TestCase):
    def test_base(self):
            cwd = os.getcwd()

            rel_global_config_dir_path = ["global"]
            rel_config_dir_path = ["config"]
            rel_ancestor_config_dir_path = ["code"]
            rel_test_assignment_dir_path = rel_ancestor_config_dir_path + ["course101", "hw1"]

            expected_out_config = {
                "course": "course101",
                "assignment": "hw1",
                "server": "http://testserver.edu",
                "user": "course-student@test.edulinq.org",
                "pass": "course-student"
            }

            expected_out_source = {
                "course":  ("<default config file>::", rel_ancestor_config_dir_path + ["autograder.json"]),
                "assignment": ("<default config file>::", rel_ancestor_config_dir_path + ["autograder.json"]),
                "server": ("<default config file>::", rel_ancestor_config_dir_path + ["autograder.json"]),
                "user": ("<default config file>::", rel_ancestor_config_dir_path + ["autograder.json"]),
                "pass": ("<default config file>::", rel_ancestor_config_dir_path + ["autograder.json"])
            }

            test_cases = [
                ([(rel_ancestor_config_dir_path, "autograder.json", DEFAULT_CONFIG, "local"), ], expected_out_config, expected_out_source),
            ]

            for test_case in test_cases:
                temp_dir = autograder.util.dirent.get_temp_path('autograder-test-config-')

                list_of_configs, expected_config_json, expected_source_json = test_case

                global_config_dir_path = [temp_dir] + rel_global_config_dir_path
                abs_global_config_dir_path = os.path.join(*global_config_dir_path)

                config_dir_path = [temp_dir] + rel_config_dir_path
                abs_config_dir_path = os.path.join(*config_dir_path)

                ancestor_config_dir_path = [temp_dir] + rel_ancestor_config_dir_path
                abs_ancestor_config_dir_path = os.path.join(*ancestor_config_dir_path)

                test_assignment_dir_path = [temp_dir] + rel_test_assignment_dir_path
                abs_test_assignment_dir_path = os.path.join(*test_assignment_dir_path)

                autograder.util.dir.mkdir(temp_dir)
                autograder.util.dir.mkdir(abs_global_config_dir_path)
                autograder.util.dir.mkdir(abs_config_dir_path)
                autograder.util.dir.mkdir(abs_ancestor_config_dir_path)
                autograder.util.dir.mkdir(abs_test_assignment_dir_path)

                config_path_list = None
                config_global_path = temp_dir

                for config_file in list_of_configs:
                    rel_path_config, name_config, data , type_config = config_file

                    abs_path_config = [temp_dir] + rel_path_config
                    write_config(data, os.path.join(*abs_path_config), name_config)

                    if type_config == "global":
                        config_global_path = os.path.join(abs_global_config_dir_path, "autograder.json")
                    elif type_config == "cli":
                        config_path_list = [os.path.join(abs_config_dir_path, name_config)]

                os.chdir(abs_test_assignment_dir_path)

                actual_configs, actual_sources = autograder.api.config.get_tiered_config(
                    argparse.Namespace(config_paths = config_path_list),
                    show_sources = True,
                    global_config_path = config_global_path
                )

                self.assertEqual(actual_configs, expected_config_json,)
                self.assertEqual(actual_sources, get_config_with_abs_path(expected_source_json, temp_dir))

            os.chdir(cwd)
