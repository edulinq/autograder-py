import typing

import autograder.wizard.commands
import autograder.wizard.model

class ConnectToServerStep(autograder.wizard.model.BaseStep):
    """ A step for connecting to an autograder server. """

    def __init__(self) -> None:
        super().__init__('Connect to Server')

    def consume_line(self, line: str, wizard: autograder.wizard.model.BaseWizard) -> bool:
        # TEST
        return False

class CourseSetupWizard(autograder.wizard.model.BaseWizard):
    """
    A wizard for setting up an autograder course.
    """

    COMMANDS: typing.Dict[typing.Tuple[str, ...], autograder.wizard.model.BaseCommand] = {
        ('?', 'h', 'help'): autograder.wizard.commands.Help(),
    }

    STEPS: typing.List[autograder.wizard.model.BaseStep] = [
        ConnectToServerStep(),
    ]

    def __init__(self):
        super().__init__(
            steps = CourseSetupWizard.STEPS,
            commands = CourseSetupWizard.COMMANDS,
        )

    def _intro(self) -> None:
        self.write("Welcome to the course setup wizard.")
        self.write("Use :? or :help to see all available commands.")
        self.write("The exit, use `:quit` or Ctrl-C twice.")
        self.write('')
