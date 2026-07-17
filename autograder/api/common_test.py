import edq.testing.unittest

import autograder.api.common
import autograder.api.constants

class TestCheckServerVersion(edq.testing.unittest.BaseTest):
    """ Test the _check_server_version helper. """

    def test_check_server_version(self):
        """ Test _check_server_version. """

        supported_version = autograder.api.constants.SUPPORTED_SERVER_VERSION
        (major, minor, patch) = supported_version.split('.')

        # [(response_body, expected compatible bool), ...]
        test_cases = [
            # Exact match - compatible.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': supported_version,
                        'git-hash': 'abc12345',
                        'is-dirty': False,
                    },
                },
                True,
            ),

            # Patch-only difference - compatible.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': f"{major}.{minor}.99",
                        'git-hash': 'abc12345',
                        'is-dirty': False,
                    },
                },
                True,
            ),

            # Minor version difference - mismatch.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': f"{major}.{int(minor) + 1}.0",
                        'git-hash': 'abc12345',
                        'is-dirty': False,
                    },
                },
                False,
            ),

            # Major version difference - mismatch.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': f"{int(major) + 1}.0.0",
                        'git-hash': 'abc12345',
                        'is-dirty': False,
                    },
                },
                False,
            ),

        ]

        for (i, test_case) in enumerate(test_cases):
            (response_body, expected) = test_case

            with self.subTest(msg = f"Case {i}:"):
                actual = autograder.api.common._check_server_version(response_body)
                self.assertEqual(expected, actual)
