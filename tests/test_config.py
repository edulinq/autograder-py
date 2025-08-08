import argparse
import os
import unittest

import autograder.api.config
import autograder.util.dir
import autograder.util.dirent

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
CONFIGS_DIR = os.path.join(THIS_DIR, "data", "configs")

class TestConfig(unittest.TestCase):
    def test_local_autograder_json_current_dir(self):
        config_dir = "simple"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": f"<default config file>:: {os.path.join('TEMP_DIR', config_dir, 'autograder.json')}"
        }

        self._evaluate_test_config(config_dir, expected_config, expected_source)

    def test_local_config_json_current_dir(self):
        config_dir = "old-name"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": f"<default config file>:: {os.path.join('TEMP_DIR', config_dir, 'config.json')}"
        }

        self._evaluate_test_config(config_dir, expected_config, expected_source)

    def test_local_ancestor_dir(self):
        config_dir = os.path.join("nested","nest1","nest2")


        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": f"<default config file>:: {os.path.join('TEMP_DIR', os.path.join('nested'), 'autograder.json')}"
        }

        self._evaluate_test_config(config_dir, expected_config, expected_source)

    def _evaluate_test_config(self, config_directory, expected_config, expected_source):
        previous_work_directory = os.getcwd()

        temp_dir = autograder.util.dir.get_temp_dir(prefix = 'autograder-test-config-')

        autograder.util.dirent.copy_contents(CONFIGS_DIR, temp_dir)

        cwd = os.path.join(temp_dir, config_directory)
        os.chdir(cwd)

        try:
            actual_configs, actual_sources = autograder.api.config.get_tiered_config(
                argparse.Namespace(config_paths = None),
                show_sources = True,
                global_config_path = temp_dir,
                local_scope = temp_dir
            )
        finally:
            os.chdir(previous_work_directory)

        for key, value in actual_sources.items():
            actual_sources[key] = value.replace(temp_dir, "TEMP_DIR")

        self.assertEqual(actual_configs, expected_config)
        self.assertEqual(actual_sources, expected_source)
