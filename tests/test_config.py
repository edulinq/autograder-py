import argparse
import unittest
import os
import json
import autograder.util.dirent
import autograder.api.config

EXPECTED_CONFIG = { 
    "course": "course101",
    "assignment": "hw1",
    "server": "http://testserver.edu",
    "user": "course-student@test.edulinq.org",
    "pass": "course-student"
}

def write_config(data, config_path, config_name = "config.json"):
    config_file = os.path.join(config_path, config_name)
    with open(config_file, 'w') as file:
        json.dump(data, file, indent = 4)

    return config_file

class TestConfig(unittest.TestCase):
    def test_base_local(self):
        temp_dir = autograder.util.dirent.get_temp_path('autograder-test-config-')
        os.mkdir(temp_dir)

        path_to_config = os.path.join(temp_dir, "path")
        os.mkdir(path_to_config)

        path_course101 = os.path.join(path_to_config, "to", "course", "course101")
        os.makedirs(path_course101, exist_ok = True)
        os.chdir(path_course101)

        config_path = write_config(EXPECTED_CONFIG, path_to_config, "autograder.json")
        expected_source = {
            "course": f"<default config file>:: {config_path}",
            "assignment": f"<default config file>:: {config_path}",
            "server": f"<default config file>:: {config_path}",
            "user": f"<default config file>:: {config_path}",
            "pass": f"<default config file>:: {config_path}"
        }

        actual_configs, actual_sources = autograder.api.config.get_tiered_config(argparse.Namespace(config_paths = None), show_sources = True, global_config_path = temp_dir)

        self.assertEqual(actual_configs, EXPECTED_CONFIG)
        self.assertEqual(actual_sources, expected_source)

        config_path = write_config(EXPECTED_CONFIG, path_course101)
        expected_source = {
            "course": f"<default config file>:: {config_path}",
            "assignment": f"<default config file>:: {config_path}",
            "server": f"<default config file>:: {config_path}",
            "user": f"<default config file>:: {config_path}",
            "pass": f"<default config file>:: {config_path}"
        }

        actual_configs, actual_sources = autograder.api.config.get_tiered_config(argparse.Namespace(config_paths = None), show_sources = True, global_config_path = temp_dir)

        self.assertEqual(actual_configs, EXPECTED_CONFIG)
        self.assertEqual(actual_sources, expected_source)

        config_path = write_config(EXPECTED_CONFIG, path_course101, "autograder.json")
        expected_source = {
            "course": f"<default config file>:: {config_path}",
            "assignment": f"<default config file>:: {config_path}",
            "server": f"<default config file>:: {config_path}",
            "user": f"<default config file>:: {config_path}",
            "pass": f"<default config file>:: {config_path}"
        }

        actual_configs, actual_sources = autograder.api.config.get_tiered_config(argparse.Namespace(config_paths = None), show_sources = True, global_config_path = temp_dir)

        self.assertEqual(actual_configs, EXPECTED_CONFIG)
        self.assertEqual(actual_sources, expected_source)


    def test_base_global(self):
        temp_dir = autograder.util.dirent.get_temp_path('autograder-test-config-')
        os.mkdir(temp_dir)

        path_global = os.path.join(temp_dir, "global")
        os.mkdir(path_global) 

        path_course101 = os.path.join(temp_dir, "course101")
        os.mkdir(path_course101)
        os.chdir(path_course101)

        config_path = write_config(EXPECTED_CONFIG, path_global, config_name = "autograder.json")

        expected_source = {
            "course": f"<user config file>:: {config_path}",
            "assignment": f"<user config file>:: {config_path}",
            "server": f"<user config file>:: {config_path}",
            "user": f"<user config file>:: {config_path}",
            "pass": f"<user config file>:: {config_path}"
        }

        actual_configs, actual_sources = autograder.api.config.get_tiered_config(argparse.Namespace(config_paths = None), show_sources = True, global_config_path = config_path)

        self.assertEqual(actual_configs, EXPECTED_CONFIG)
        self.assertEqual(actual_sources, expected_source)

    def test_base_cli_config(self):
        temp_dir = autograder.util.dirent.get_temp_path('autograder-test-config-')
        os.mkdir(temp_dir)

        path_to_config = os.path.join(temp_dir, "path", "to", "config")
        os.makedirs(path_to_config, exist_ok = True)

        path_course101 = os.path.join(temp_dir, "course101")
        os.mkdir(path_course101)
        os.chdir(path_course101)

        config_path = write_config(EXPECTED_CONFIG, path_to_config)

        expected_source = {
            "course": f"<cli config file>:: {config_path}",
            "assignment": f"<cli config file>:: {config_path}",
            "server": f"<cli config file>:: {config_path}",
            "user": f"<cli config file>:: {config_path}",
            "pass": f"<cli config file>:: {config_path}"
        }

        actual_configs, actual_sources = autograder.api.config.get_tiered_config(argparse.Namespace(config_paths = [config_path]), show_sources = True, global_config_path = temp_dir)

        self.assertEqual(actual_configs, EXPECTED_CONFIG)
        self.assertEqual(actual_sources, expected_source)

    def test_all(self):
        temp_dir = autograder.util.dirent.get_temp_path('autograder-test-config-')
        os.mkdir(temp_dir)

        path_course101 = os.path.join(temp_dir, "course101")
        os.mkdir(path_course101)

        path_global = os.path.join(temp_dir, "global")
        os.mkdir(path_global) 

        path_to_config = os.path.join(temp_dir, "path", "to", "config")
        os.makedirs(path_to_config, exist_ok = True)

        write_config(EXPECTED_CONFIG, path_course101, "autograder.json")
        global_config_path = write_config(EXPECTED_CONFIG, path_global, "autograder.json")
        config_path  =  write_config(EXPECTED_CONFIG, path_to_config, "config.json")

        expected_source = {
            "course": f"<cli config file>:: {config_path}",
            "assignment": f"<cli config file>:: {config_path}",
            "server": f"<cli config file>:: {config_path}",
            "user": f"<cli config file>:: {config_path}",
            "pass": f"<cli config file>:: {config_path}"
        }

        os.chdir(path_course101)
        actual_configs, actual_sources = autograder.api.config.get_tiered_config(argparse.Namespace(config_paths = [config_path]), show_sources = True, global_config_path = global_config_path)

        self.assertEqual(actual_configs, EXPECTED_CONFIG)
        self.assertEqual(actual_sources, expected_source) 




