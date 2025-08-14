import argparse
import os
import tests.base

import autograder.api.config
import autograder.util.dir
import autograder.util.dirent

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
CONFIGS_DIR = os.path.join(THIS_DIR, "data", "configs")

class TestConfig(tests.base.BaseTest):
    def test_base(self):
        test_cases = [
            (
                "simple",
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<local config file>::{os.path.join('TEMP_DIR', 'simple', 'autograder.json')}"
                },
                "",
                None
            ),
            (
                "old-name",
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<local config file>::{os.path.join('TEMP_DIR', 'old-name', 'config.json')}"
                },
                "",
                None
            ),
            (
                os.path.join("nested", "nest1", "nest2a"),
                {
                    "server": "http://test.edulinq.org"
                },
                {
                    "server": f"<local config file>::{os.path.join('TEMP_DIR', 'nested', 'autograder.json')}"
                },
                "",
                None
            ),
            (
                os.path.join("nested", "nest1", "nest2b"),
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<local config file>::{os.path.join('TEMP_DIR', 'nested', 'nest1', 'nest2b', 'autograder.json')}"
                },
                "",
                None
            ),
            (
                "empty-dir",
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<global config file>::{os.path.join('TEMP_DIR', 'global', 'autograder.json')}"
                },
                os.path.join("global", "autograder.json"),
                None
            ),
            (
                "empty-dir",
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<cli config file>::{os.path.join('TEMP_DIR', 'simple', 'autograder.json')}"
                },
                "",
                [
                    os.path.join("global", "autograder.json"),
                    os.path.join("simple", "autograder.json")
                ]
            ),
            (
                "empty-dir",
                {
                    "user": "user@test.edulinq.org",
                    "server": "http://test.edulinq.org"
                },
                {
                    "user": f"<cli config file>::{os.path.join('TEMP_DIR', 'simple', 'autograder.json')}",
                    "server": f"<cli config file>::{os.path.join('TEMP_DIR', 'nested', 'autograder.json')}"
                },
                "",
                [
                    os.path.join("nested", "autograder.json"),
                    os.path.join("simple", "autograder.json")
                ]
            ),
            (
                "simple",
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<local config file>::{os.path.join('TEMP_DIR', 'simple', 'autograder.json')}"
                },
                os.path.join("global", "autograder.json"),
                None
            ),
            (
                "empty-dir",
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<cli config file>::{os.path.join('TEMP_DIR', 'simple', 'autograder.json')}"
                },
                os.path.join("global", "autograder.json"),
                [os.path.join("simple", "autograder.json")]
            ),
            (
                "simple",
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<cli config file>::{os.path.join('TEMP_DIR', 'old-name', 'config.json')}"
                },
                "",
                [os.path.join("old-name", "config.json")]
            ),
            (
                "simple",
                {
                    "user": "user@test.edulinq.org"
                },
                {
                    "user": f"<cli config file>::{os.path.join('TEMP_DIR', 'old-name', 'config.json')}"
                },
                os.path.join("global", "autograder.json"),
                [os.path.join("old-name", "config.json")]
            )
        ]

        for test_case in test_cases:
            (test_work_dir, expected_config, expected_source, config_global, config_paths) = test_case

            self._evaluate_test_config(
                test_work_dir, expected_config,
                expected_source, config_global, config_paths
            )

    def _evaluate_test_config(
            self, test_work_dir, expected_config,
            expected_source, global_config_path = None,
            config_paths = None):
        """
        Prepares testing environment and normalizes cli config paths,
        global config path and expected source paths. Evaluates the given expected and
        source configs with actual get_tiered_config() output.
        """

        temp_dir = autograder.util.dir.get_temp_dir(prefix = 'autograder-test-config-')
        global_config = os.path.join(temp_dir)

        if (global_config_path is not None):
            global_config = os.path.join(temp_dir, global_config_path)

        abs_config_paths = []
        if (config_paths is not None):
            for rel_config_path in config_paths:
                abs_config_paths.append(os.path.join(temp_dir, rel_config_path))
   
        autograder.util.dirent.copy_contents(CONFIGS_DIR, temp_dir)

        previous_work_directory = os.getcwd()
        initial_work_directory = os.path.join(temp_dir, test_work_dir)
        os.chdir(initial_work_directory)

        try:
            actual_configs, actual_sources = autograder.api.config.get_tiered_config(
                argparse.Namespace(config_paths = abs_config_paths),
                global_config_path = global_config,
                local_config_root_cutoff = temp_dir
            )
        finally:
            os.chdir(previous_work_directory)

        for (key, value) in actual_sources.items():
            actual_sources[key] = value.replace(temp_dir, "TEMP_DIR")

        self.assertDictEqual(actual_configs, expected_config)
        self.assertDictEqual(actual_sources, expected_source)
