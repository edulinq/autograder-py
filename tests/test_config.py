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
        work_dir = "simple"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": (
                "<default config file>:: %s"
                % os.path.join('TEMP_DIR', 'simple', 'autograder.json')
            )
        }

        self._evaluate_test_config(work_dir, expected_config, expected_source)

    def test_local_config_json_current_dir(self):
        work_dir = "old-name"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": (
                "<default config file>:: %s"
                % os.path.join('TEMP_DIR', 'old-name', 'config.json')
            )
        }

        self._evaluate_test_config(work_dir, expected_config, expected_source)

    def test_local_ancestor_dir(self):
        work_dir = os.path.join("nested", "nest1", "nest2.1")

        expected_config = {
            "server": "http://testserver.edu"
        }

        expected_source = {
            "server": (
                "<default config file>:: %s"
                % os.path.join('TEMP_DIR', 'nested', 'autograder.json')
            )
        }

        self._evaluate_test_config(work_dir, expected_config, expected_source)

    def test_local_all(self):
        work_dir = os.path.join("nested", "nest1", "nest2.2")

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": "%s %s" % (
                "<default config file>::",
                os.path.join(
                    "TEMP_DIR",
                    "nested",
                    "nest1",
                    "nest2.2",
                    "autograder.json"
                )
            )
        }

        self._evaluate_test_config(work_dir, expected_config, expected_source)

    def test_global(self):
        work_dir = "empty-dir"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": (
                "<user config file>:: %s"
                % os.path.join('TEMP_DIR', 'global', 'autograder.json')
            )
        }

        self._evaluate_test_config(
            work_dir, expected_config,
            expected_source, config_global = os.path.join("global", "autograder.json")
        )

    def test_cli_provided_overriding(self):
        work_dir = "empty-dir"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": (
                "<cli config file>:: %s"
                % os.path.join('TEMP_DIR', 'simple', 'autograder.json')
            )
        }

        list_config_paths = [
            os.path.join("global", "autograder.json"),
            os.path.join("simple", "autograder.json")
        ]

        self._evaluate_test_config(
            work_dir, expected_config,
            expected_source, config_paths = list_config_paths
        )

    def test_cli_provided(self):
        work_dir = "empty-dir"

        expected_config = {
            "user": "user@test.edulinq.org",
            "server": "http://testserver.edu"
        }

        expected_source = {
            "user": (
                "<cli config file>:: %s"
                % os.path.join('TEMP_DIR', 'simple', 'autograder.json')
            ),
            "server": (
                "<cli config file>:: %s"
                % os.path.join('TEMP_DIR', 'nested', 'autograder.json')
            )
        }

        list_config_paths = [
            os.path.join("nested", "autograder.json"),
            os.path.join("simple", "autograder.json")
        ]

        self._evaluate_test_config(
            work_dir, expected_config,
            expected_source, config_paths = list_config_paths
        )

    def test_global_local(self):
        work_dir = "simple"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": (
                "<default config file>:: %s"
                % os.path.join('TEMP_DIR', 'simple', 'autograder.json')
            )
        }

        self._evaluate_test_config(
            work_dir, expected_config,
            expected_source, config_global = os.path.join("global", "autograder.json")
        )

    def test_cli_global(self):
        work_dir = "empty-dir"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": (
                "<cli config file>:: %s"
                % os.path.join('TEMP_DIR', 'simple', 'autograder.json')
            )
        }

        list_config_paths = [os.path.join("simple", "autograder.json")]

        self._evaluate_test_config(
            work_dir, expected_config, expected_source,
            config_global = os.path.join("global", "autograder.json"),
            config_paths = list_config_paths
        )

    def test_local_cli(self):
        work_dir = "simple"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": (
                "<cli config file>:: %s"
                % os.path.join('TEMP_DIR', 'old-name', 'config.json')
            )
        }

        list_config_paths = [os.path.join("old-name", "config.json")]

        self._evaluate_test_config(
            work_dir, expected_config,
            expected_source, config_paths = list_config_paths
        )

    def test_all(self):
        work_dir = "simple"

        expected_config = {
            "user": "user@test.edulinq.org"
        }

        expected_source = {
            "user": (
                "<cli config file>:: %s"
                % os.path.join('TEMP_DIR', 'old-name', 'config.json')
            )
        }

        list_config_paths = [os.path.join("old-name", "config.json")]

        self._evaluate_test_config(
            work_dir, expected_config, expected_source,
            config_global = os.path.join("global", "autograder.json"),
            config_paths = list_config_paths
        )

    def _evaluate_test_config(
            self, test_work_dir, expected_config,
            expected_source, config_global = "",
            config_paths = None):
        """
        Prepares testing environment while normalizes cli config paths,
        global config path and expected source paths. Evaluates the given expected and
        source configs with actual get_tiered_config() output.
        """

        previous_work_directory = os.getcwd()

        temp_dir = autograder.util.dir.get_temp_dir(prefix = 'autograder-test-config-')
        global_config = os.path.join(temp_dir, config_global)

        abs_config_paths = []
        if config_paths is not None:
            for rel_config_path in config_paths:
                abs_config_paths.append(os.path.join(temp_dir, rel_config_path))

        autograder.util.dirent.copy_contents(CONFIGS_DIR, temp_dir)

        cwd = os.path.join(temp_dir, test_work_dir)
        os.chdir(cwd)

        try:
            actual_configs, actual_sources = autograder.api.config.get_tiered_config(
                argparse.Namespace(config_paths = abs_config_paths),
                show_sources = True,
                global_config_path = global_config,
                local_scope = temp_dir
            )
        finally:
            os.chdir(previous_work_directory)

        for key, value in actual_sources.items():
            actual_sources[key] = value.replace(temp_dir, "TEMP_DIR")

        self.assertEqual(actual_configs, expected_config)
        self.assertEqual(actual_sources, expected_source)
