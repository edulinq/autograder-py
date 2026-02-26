import autograder.wizard.model

class EchoStep(autograder.wizard.model.BaseStep):
    """ A debugging step that just echo's back the current line and never ends. """

    def __init__(self) -> None:
        super().__init__('Echo')

        self.line: str = ''
        """ The last seen line. """

    def status_line(self) -> str:
        return self.line

    def consume_line(self, line: str, wizard: autograder.wizard.model.BaseWizard) -> bool:
        self.line = line

        wizard.write(line)

        return False
