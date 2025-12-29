import autograder.api.config
import autograder.api.metadata.describe
import autograder.testing.asserts
import autograder.testing.model
import autograder.testing.server

class TestDescribe(autograder.testing.server.ServerTest):
    """ Test describing the API. """

    def test_base(self):
        """ Test base functionality. """

        api_description = autograder.testing.asserts.get_expected_api_description()

        # [(config (and overrides), kwargs, expected, error substring), ...]
        test_cases = [
            (
                {},
                {},
                api_description,
                None,
            ),
            (
                {
                    'force_compute': True,
                },
                {},
                api_description,
                None,
            ),
        ]

        self.base_api_test(autograder.api.metadata.describe.send, test_cases)
