"""
Common wizard commands.
"""

import typing

import autograder.wizard.model

# TODO - jump

# TODO - replay?

# TODO - clear screen

class Help(autograder.wizard.model.BaseCommand):
    """ Output help for this wizard. """

    def __init__(self) -> None:
        super().__init__("Output help for this wizaard.")

    def run(self, wizard: autograder.wizard.model.BaseWizard, argument: typing.Union[str, None]) -> None:
        wizard._help()

class Status(autograder.wizard.model.BaseCommand):
    """ Output status for this wizard. """

    def __init__(self) -> None:
        super().__init__("Output status of each step for this wizaard.")

    def run(self, wizard: autograder.wizard.model.BaseWizard, argument: typing.Union[str, None]) -> None:
        wizard._status()
