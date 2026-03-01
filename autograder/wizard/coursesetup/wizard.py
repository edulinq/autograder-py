import typing

import autograder.api.config
import autograder.api.metadata.heartbeat
import autograder.error
import autograder.wizard.commands
import autograder.wizard.model
import autograder.wizard.steps

class SetupData:
    """ A container for all the data used in this wizard. """

    def __init__(self, config: typing.Dict[str, typing.Any]) -> None:
        self.server: typing.Union[str, None] = config.get(autograder.api.config.PARAM_SERVER.config_key, None)
        """ The server to connect to. """

        self.user: typing.Union[str, None] = config.get(autograder.api.config.PARAM_USER_EMAIL.config_key, None)
        """ The user to connect as. """

        self.password: typing.Union[str, None] = config.get(autograder.api.config.PARAM_USER_PASS.config_key, None)
        """ The password to connect with. """

class ConnectStep(autograder.wizard.steps.SimpleInputStep):
    """ A step for connecting to an autograder server. """

    def __init__(self, data: SetupData) -> None:
        self._server_input: autograder.wizard.steps.SimpleInput = autograder.wizard.steps.SimpleInput(
            'address',
            'Enter the server to connect to',
            data.server,
        )

        self.data: SetupData = data
        """ The common data for this wizard. """

        super().__init__('Connect to Server', [
            self._server_input,
        ])

    def post_input_action(self, wizard: autograder.wizard.model.BaseWizard) -> bool:
        server = self._server_input.value

        try:
            autograder.api.metadata.heartbeat.send({
                autograder.api.config.PARAM_SERVER.config_key: server,
            })
        except autograder.error.ConnectionError:
            wizard.write(f"Could not connect to autograder server at '{server}', check address and that the server is up.")
            return False

        self.data.server = server
        wizard.write(f"Successfully connected to autograder server at '{server}'.")

        return True

class CourseSetupWizard(autograder.wizard.model.BaseWizard):
    """
    A wizard for setting up an autograder course.
    """

    def __init__(self, config: typing.Dict[str, typing.Any]):
        self.data: SetupData = SetupData(config)
        """ The common data for this wizard. """

        steps: typing.List[autograder.wizard.model.BaseStep] = [
            ConnectStep(self.data),
            # AuthStep(self.data),
            # Source
            # Build
            # Save / Commit

            # TEST
            autograder.wizard.steps.EchoStep(),
        ]

        super().__init__(
            steps = steps,
            commands = autograder.wizard.commands.COMMON_COMMANDS,
        )

    def _intro(self) -> None:
        self.write("Welcome to the course setup wizard.")
        self.write("Use :? or :help to see all available commands.")
        self.write("The exit, use `:quit` or Ctrl-C twice.")
        self.write('')
