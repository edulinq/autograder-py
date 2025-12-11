import autograder.api.config
import autograder.api.users.list
import autograder.testing.server

class TestUsersList(autograder.testing.server.ServerTest):
    def test_base(self):
        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            (
                {
                },
                [
                ],
                None,
            ),
        ]

        self.base_api_test(autograder.api.users.list.send, test_cases)
