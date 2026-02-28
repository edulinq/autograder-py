import typing

import autograder.api.config
import autograder.api.metadata.heartbeat
import autograder.error
import autograder.wizard.commands
import autograder.wizard.model
import autograder.wizard.steps

class SetupData:
    """ A container for all the data used in this wizard. """

    def __init__(self,
            server: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        self.server: typing.Union[str, None] = server
        """ The server to connect to. """

class ConnectToServerStep(autograder.wizard.model.BaseStep):
    """ A step for connecting to an autograder server. """

    def __init__(self, data: SetupData) -> None:
        super().__init__('Connect to Server')

        self.data: SetupData = data
        """ The common data for this wizard. """

    def get_prompt(self) -> typing.Union[str, None]:
        suffix = ''
        if (self.data.server is not None):
            suffix = f" (or nothing to use '{self.data.server}')"

        return f"Enter the server to connect to{suffix}: "

    def status_line(self) -> str:
        if (self.data.server is None):
            return ''

        return self.data.server

    def consume_line(self, line: str, wizard: autograder.wizard.model.BaseWizard) -> bool:
        server: typing.Union[str, None] = line
        if ((server is not None) and (len(line) == 0)):
            server = self.data.server

        if (server is None):
            return False

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
        self.data: SetupData = SetupData(**config)
        """ The common data for this wizard. """

        steps: typing.List[autograder.wizard.model.BaseStep] = [
            ConnectToServerStep(self.data),
            # Auth
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
