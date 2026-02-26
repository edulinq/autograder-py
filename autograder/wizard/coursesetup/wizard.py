import typing

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
        if (len(line) != 0):
            self.data.server = line

        return (self.data.server is not None)

class CourseSetupWizard(autograder.wizard.model.BaseWizard):
    """
    A wizard for setting up an autograder course.
    """

    COMMANDS: typing.Dict[typing.Tuple[str, ...], autograder.wizard.model.BaseCommand] = {
        ('?', 'h', 'help'): autograder.wizard.commands.Help(),
        ('s', 'status'): autograder.wizard.commands.Status(),
    }

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
            commands = CourseSetupWizard.COMMANDS,
        )

    def _intro(self) -> None:
        self.write("Welcome to the course setup wizard.")
        self.write("Use :? or :help to see all available commands.")
        self.write("The exit, use `:quit` or Ctrl-C twice.")
        self.write('')
