import abc
import typing

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

@typing.runtime_checkable
class SimpleInputValidator(typing.Protocol):
    """ A function for checking the validity of a simple input value. """

    def __call__(self, value: str) -> typing.Union[str, None]:
        """
        Check if the given value is valid for this input.
        """

def email_simple_input_validator(value: str) -> typing.Union[str, None]:
    """ Check if the given input looks like an email. """

    if ('@' in value):
        return None

    return f"value '{value}' does not look like an email address"

class SimpleInput:
    """ A representation of simple input prompt/value. """

    def __init__(self,
            name: str,
            prompt: str,
            default: typing.Union[str, None] = None,
            validation_func: typing.Union[SimpleInputValidator, None] = None,
            ) -> None:
        self.name: str = name
        """
        The name for this input.
        Used in the status line.
        """

        self.prompt: str = prompt
        """ The prompt for this input. """

        self.default: typing.Union[str, None] = default
        """ The default value for this input. """

        self.value: typing.Union[str, None] = None
        """ The current value for this input. """

        self.validation_func: typing.Union[SimpleInputValidator, None] = validation_func
        """ The optional function to use for validation. """

    def get_current_value(self) -> typing.Union[str, None]:
        """ Get the current value (or default) for this input. """

        if (self.value is None):
            return self.default

        return self.value

    def status_string(self) -> typing.Union[str, None]:
        """
        Get a string to represent this input in a status line,
        or None if it should not be represented.
        """

        if (self.value is None):
            return None

        return f"{self.name}: {self.value}"

    def validate(self, value: str) -> typing.Union[str, None]:
        """
        Check if the given value is valid.
        If valid, return None.
        Otherwise, return a string describing the reason the value is invalid.
        """

        if (self.validation_func is None):
            return None

        return self.validation_func(value)

class SimpleInputStep(autograder.wizard.model.BaseStep):
    """
    An abstract base step that prompts for specific inputs and then executes an action.
    """

    def __init__(self,
            name: str,
            inputs: typing.List[SimpleInput],
            ) -> None:
        super().__init__(name)

        if (len(inputs) == 0):
            raise ValueError('At least one input must be provided.')

        self.inputs: typing.List[SimpleInput] = inputs
        """ The inputs this step is looking for. """

        self._current_input_index: int = 0
        """ The current input being looked for. """

    def reset(self) -> None:
        self._current_input_index = 0

        for simple_input in self.inputs:
            simple_input.value = None

    def get_prompt(self) -> typing.Union[str, None]:
        current_input = self.inputs[self._current_input_index]

        suffix = ''
        current_value = current_input.get_current_value()
        if (current_value is not None):
            suffix = f" (or nothing to use '{current_value}')"

        return f"{current_input.prompt}{suffix}: "

    def status_line(self) -> str:
        pairs = []
        for simple_input in self.inputs:
            text = simple_input.status_string()
            if (text is not None):
                pairs.append(text)

        if (len(pairs) == 0):
            return ''

        return ', '.join(pairs)

    def consume_line(self, line: str, wizard: autograder.wizard.model.BaseWizard) -> bool:
        current_input = self.inputs[self._current_input_index]

        # Collect the entered value from the line (or a default value).
        current_value: typing.Union[str, None] = line
        if ((current_value is not None) and (len(line) == 0)):
            current_value = current_input.get_current_value()

        # If nothing was collected, repeat this input.
        if (current_value is None):
            return False

        # A value was collected for this input, validate it.
        error = current_input.validate(current_value)
        if (error is not None):
            wizard.write(f"Invalid Input: {error}.")
            return False

        # The input is valid.
        current_input.value = current_value

        # Move to the next input.
        self._current_input_index += 1
        self._current_input_index = (self._current_input_index % len(self.inputs))

        # Request more inputs if there are some left.
        if (self._current_input_index != 0):
            return False

        # All inputs have been set, take the post-input action.
        # Note that the current input is set to the beginning,
        # so a failure (false) here means that this step will start from the beginning.
        return self.post_input_action(wizard)

    @abc.abstractmethod
    def post_input_action(self, wizard: autograder.wizard.model.BaseWizard) -> bool:
        """
        Take an action after all input has been gathered.
        Return true if the step is complete.
        If false is returned, the step will start again from the first input
        (but will retain the values from the previous round).
        """
