import autograder.api.config
import autograder.api.metadata.heartbeat
import autograder.testing.asserts
import autograder.testing.model
import autograder.testing.server

class TestHeartbeat(autograder.testing.server.ServerTest):
    """ Test getting a heartbeat. """

    def test_base(self):
        """ Test base functionality. """

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            (
                {
                    autograder.api.config.PARAM_USER_EMAIL.config_key: 'course-owner@test.edulinq.org',
                    autograder.api.config.PARAM_USER_PASS.config_key: 'course-owner',
                },
                {},
                {
                    'server-version': {
                        'base-version': autograder.testing.constants.TEST_BASE_VERSION,
                        'git-hash': autograder.testing.constants.TEST_GIT_HASH,
                        'is-dirty': autograder.testing.constants.TEST_IS_DIRTY,
                    },
                },
                None,
            ),
        ]

        self.base_api_test(autograder.api.metadata.heartbeat.send, test_cases, actual_clean_func = autograder.testing.asserts.normalize_dict)
