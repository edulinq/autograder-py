import os

import edq.testing.cli

import autograder.testing.server

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..')

CLI_TESTDATA_DIR: str = os.path.join(ROOT_DIR, 'autograder', 'cli', 'testdata')
CLI_TESTS_DIR: str = os.path.join(CLI_TESTDATA_DIR, 'tests')
CLI_DATA_DIR: str = os.path.join(CLI_TESTDATA_DIR, 'data')
CLI_GLOBAL_CONFG_PATH: str = os.path.join(CLI_DATA_DIR, 'testing-autograder.json')

class CLITest(autograder.testing.server.ServerTest):
    """
    CLI tests that build upon server tests.
    """

    def modify_cli_test_info(self, test_info: edq.testing.cli.CLITestInfo) -> None:
        """ Adjust the CLI test info to include core info (like server information). """

        test_info.arguments += [
            '--config-global', CLI_GLOBAL_CONFG_PATH,
            '--config', f"server={self.get_server_url()}",
        ]

    @classmethod
    def get_test_basename(cls, path: str) -> str:
        """ Get the test's name based off of its filename and location. """

        path = os.path.abspath(path)

        name = os.path.splitext(os.path.basename(path))[0]

        # Clean drive identifiers (for Windows).
        cli_tests_dir_path = os.path.splitdrive(os.path.abspath(CLI_TESTS_DIR))[1]
        path = os.path.splitdrive(path)[1]

        ancestors = os.path.dirname(path).replace(cli_tests_dir_path, '')
        prefix = ancestors.replace(os.sep, '_')

        if (prefix.startswith('_')):
            prefix = prefix.replace('_', '', 1)

        if (len(prefix) > 0):
            name =  f"{prefix}_{name}"

        return name

# Attach CLI tests.
edq.testing.cli.discover_test_cases(CLITest, CLI_TESTS_DIR, CLI_DATA_DIR)
