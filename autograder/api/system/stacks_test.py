import autograder.api.config
import autograder.api.system.stacks
import autograder.testing.server

class TestSystemStacks(autograder.testing.server.ServerTest):
    """ Test getting system stack traces. """

    def test_base(self):
        """ Test base functionality. """

        args = {
            autograder.api.config.PARAM_SERVER.config_key: self.get_server_url(),
            autograder.api.config.PARAM_USER_EMAIL.config_key: 'server-admin@test.edulinq.org',
            autograder.api.config.PARAM_USER_PASS.config_key: 'server-admin',
        }

        result = autograder.api.system.stacks.send(args)

        self.assertGreater(result['count'], 5)
        self.assertEqual(result['count'], len(result['stacks']))
