"""
Common wizard commands.
"""

import typing

import autograder.wizard.model

# TEST - Commands: ?/h, jump?, back?, replay?, clear screen, ...
#      - Prefix with colon? :h :? :b :r :c

# TEST - Command: status of the wizard? Summary/status for each step?

class Help(autograder.wizard.model.BaseCommand):
    """ Output help for this wizard. """

    def __init__(self) -> None:
        super().__init__("Output help for this wizaard.")

    def run(self, wizard: autograder.wizard.model.BaseWizard, argument: typing.Union[str, None]) -> None:
        wizard._help()
