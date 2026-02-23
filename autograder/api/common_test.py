import edq.testing.unittest

import autograder.api.common
import autograder.api.constants

class TestCheckServerVersion(edq.testing.unittest.BaseTest):
    """ Test the _check_server_version helper in autograder.api.common. """

    def test_check_server_version(self):
        """ Test that _check_server_version returns True on major/minor mismatch, False otherwise. """

        supported_version: str = autograder.api.constants.SUPPORTED_SERVER_VERSION
        supported_parts = supported_version.split('.')

        patch_only_version: str = f"{supported_parts[0]}.{supported_parts[1]}.99"
        minor_bump_version: str = f"{supported_parts[0]}.{int(supported_parts[1]) + 1}.0"
        major_bump_version: str = f"{int(supported_parts[0]) + 1}.0.0"

        # [(response_body, expected mismatch bool), ...]
        test_cases = [

            # Exact match - no mismatch.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': supported_version,
                        'git-hash': 'abc12345',
                        'is-dirty': False,
                    },
                },
                False,
            ),

            # Patch-only difference - no mismatch.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': patch_only_version,
                        'git-hash': 'abc12345',
                        'is-dirty': False,
                    },
                },
                False,
            ),

            # Minor version difference - mismatch.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': minor_bump_version,
                        'git-hash': 'abc12345',
                        'is-dirty': False,
                    },
                },
                True,
            ),

            # Major version difference - mismatch.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': major_bump_version,
                        'git-hash': 'abc12345',
                        'is-dirty': False,
                    },
                },
                True,
            ),

            # Missing server-version key - no mismatch.
            (
                {},
                False,
            ),

            # None base-version - no mismatch.
            (
                {
                    autograder.api.constants.API_RESPONSE_KEY_SERVER_VERSION: {
                        'base-version': None,
                        'git-hash': '',
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
