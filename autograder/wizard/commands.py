"""
Common wizard commands.
"""

import typing

import autograder.wizard.model

# TODO - jump

# TODO - replay?

class Clear(autograder.wizard.model.BaseCommand):
    """ clear the screen for this wizard. """

    def __init__(self) -> None:
        super().__init__("Clear the screen.")

    def run(self, wizard: autograder.wizard.model.BaseWizard, argument: typing.Union[str, None]) -> None:
        wizard._clear()

class Help(autograder.wizard.model.BaseCommand):
    """ Output help for this wizard. """

    def __init__(self) -> None:
        super().__init__("Output help information.")

    def run(self, wizard: autograder.wizard.model.BaseWizard, argument: typing.Union[str, None]) -> None:
        wizard._help()

class Status(autograder.wizard.model.BaseCommand):
    """ Output status for this wizard. """

    def __init__(self) -> None:
        super().__init__("Output the status of each step.")

    def run(self, wizard: autograder.wizard.model.BaseWizard, argument: typing.Union[str, None]) -> None:
        wizard._status()

COMMON_COMMANDS: typing.Dict[typing.Tuple[str, ...], autograder.wizard.model.BaseCommand] = {
    ('?', 'h', 'help'): Help(),
    ('s', 'status'): Status(),
    ('c', 'clear'): Clear(),
}
