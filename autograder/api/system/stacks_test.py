import autograder.api.config
import autograder.api.system.stacks
import autograder.model.config
import autograder.testing.server

class TestSystemStacks(autograder.testing.server.ServerTest):
    """ Test getting system stack traces. """

    def test_base(self) -> None:
        """ Test base functionality. """

        config = args = autograder.model.config.Config(
            server = self.get_server_url(),
            auth_user = 'server-admin@test.edulinq.org',
            auth_pass = 'server-admin',
        )

        result = autograder.api.system.stacks.send(args)

        self.assertGreater(result['count'], 5)
        self.assertEqual(result['count'], len(result['stacks']))
