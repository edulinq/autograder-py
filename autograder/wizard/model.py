import abc
import io
import os
import re
import sys
import typing

import autograder.util.terminal

DEFAULT_COMMAND_PREFIX: str = ':'
DEFAULT_INDENT: str = '    '
DEFAULT_PROMPT_TEXT: str = '$ '

class BaseStep(abc.ABC):
    """
    A step in a wizard (a state in the wizard's FSM).

    Note that each step can carry data with it that may represent the actions taken on that step.
    For example, if a user entered information on that step.
    This means that instances of a step stays alive for the duration of the wizard
    (a new instance is not created each time the step is entered).
    """

    def __init__(self, name: str) -> None:
        name = name.strip()
        if (len(name) == 0):
            raise ValueError('Step name must be non-empty.')

        self.name: str = name
        """ A name to refer to this step. """

    def get_prompt(self) -> typing.Union[str, None]:
        """
        Get the text prompt to use.
        Falls back to the default wizard prompt.
        """

        return None

    def intro(self, wizard: 'BaseWizard') -> None:
        """ Called when transitioning into this step. """

    def outro(self, wizard: 'BaseWizard') -> None:
        """
        Called when transitioning out of this step.
        Is not called when exiting early.
        """

    def status_line(self) -> str:
        """
        Get a line to display about the status of this step.
        This will display when the wizard wants a summary of all steps.
        """

        return ''

    def reset(self) -> None:
        """
        Clear all the state associated with this step.
        Used in cases such as when a user goes backwards in the wizard.
        """

    @abc.abstractmethod
    def consume_line(self, line: str, wizard: 'BaseWizard') -> bool:
        """
        Consume the current line of input.
        Return true if the step is complete.
        """

class BaseCommand(abc.ABC):
    """
    A command that can be run at any step in the wizard.
    """

    def __init__(self, help_line: str) -> None:
        self.help_line = help_line
        """ The line to use when this command is output to a help prompt. """

    @abc.abstractmethod
    def run(self, wizard: 'BaseWizard', argument: typing.Union[str, None]) -> None:
        """ Run the command on the given wizard. """

class BaseWizard(abc.ABC):
    """
    The base class for a CLI wizard.

    A wizard is a tool that guides a users through a series of steps,
    most often seen for software installers.
    See: https://en.wikipedia.org/wiki/Wizard_(software) .

    This class represents a wizard as finite state machine (FSM).
    See: https://en.wikipedia.org/wiki/Finite-state_machine .
    Specifically, the wizard's FSM must be linear and go through states sequentially.
    """

    def __init__(self,
            steps: typing.List[BaseStep],
            commands: typing.Union[typing.Dict[typing.Tuple[str, ...], BaseCommand], None] = None,
            help_command_key: typing.Union[str, None] = None,
            command_prefix: str = DEFAULT_COMMAND_PREFIX,
            reader: typing.Union[io.TextIOBase, None] = None,
            writer: typing.Union[io.TextIOBase, None] = None,
            indent: str = DEFAULT_INDENT,
            prompt_text: str = DEFAULT_PROMPT_TEXT,
            **kwargs: typing.Any) -> None:
        if (reader is None):
            reader = typing.cast(io.TextIOBase, sys.stdin)

        self.reader: io.TextIOBase = reader
        """
        The input stream to read from.
        Defaults to stdin.
        """

        if (writer is None):
            writer = typing.cast(io.TextIOBase, sys.stdout)

        self.writer: io.TextIOBase = writer
        """
        The input stream to write to.
        Defaults to stdout.
        """

        if ((steps is None) or (len(steps) == 0)):
            raise ValueError("Wizards need at least one step.")

        self.steps: typing.List[BaseStep] = steps

        if (commands is None):
            commands = {}

        self.commands: typing.Dict[typing.Tuple[str, ...], BaseCommand] = commands
        """
        The commands to use in this wizard.
        Commands can be supplied at any step in the wizard.

        This dict maps all text keys for a command (excluding the prefix) to the command itself.
        The tuple of keys allow for command aliases (e.g. ('?', 'h', 'help')).
        """

        self.help_command_key: typing.Union[str, None] = help_command_key
        """
        The key for the help command (if one exists).
        This can be used to help prompt the user when they make a mistake.
        """

        self.command_prefix: str = command_prefix
        """ The prefix to identify a command line. """

        self.indent: str = DEFAULT_INDENT
        """ The suggested indentation to use. """

        self.prompt_text: str = prompt_text
        """ The text to use to indicate a prompt. """

        self.has_read_line: bool = True
        """
        Indicates that a line has been read since the last time a Ctrl-C was seen.
        Intentionally starts at true to make the initial case consistent.
        """

    def run(self) -> None:
        """ Run the wizard. """

        self.intro()

        exit_early = False
        current_step_index: typing.Union[int, None] = self._transition(None)

        while ((current_step_index is not None) and (not exit_early)):
            try:
                (current_step_index, exit_early) = self._run_loop(current_step_index)
            except EOFError:
                # If we got an EOF (or Ctrl-D), just exit.
                self.write('')
                self.write("Reached end of input, exiting.")
                return
            except KeyboardInterrupt:
                # If this is the first Ctrl-C since the last input, just clear the line and wait.
                # Otherwise, exit.
                self.write('')

                if (not self.has_read_line):
                    self.write("Caught keyboard interrupt, exiting.")
                    return

                self.write("Caught keyboard interrupt, press once more to exit.")
                self.has_read_line = False

        if (exit_early):
            self.early_exit()
        else:
            self.outro()

    def _run_loop(self, current_step_index: typing.Union[int, None]) -> typing.Tuple[typing.Union[int, None], bool]:
        """
        The main control loop for the wizard.

        Returns the current step index and whether or not the wizard should exit early.
        """

        while (current_step_index is not None):
            current_step = self.steps[current_step_index]

            # Get the next line of input.
            line = self.read_line(step_prompt = current_step.get_prompt())
            if (line is None):
                return current_step_index, True

            # Check if the line is a command.
            line_consumed = self.check_and_run_command(line)
            if (line_consumed):
                continue

            # Pass the line to the current step.
            step_complete = current_step.consume_line(line, self)
            if (not step_complete):
                continue

            # The step ran and is complete, transition to the next step.
            current_step_index = self._transition(current_step_index)

        return current_step_index, False

    def write(self, text: str, newline: bool = True, flush: bool = False) -> None:
        """
        Write text to the wizard's writer.
        """

        self.writer.write(text)

        if (newline):
            self.writer.write(os.linesep)

        if (flush):
            self.writer.flush()

    def get_input(self, text: str, check_command: bool = True) -> str:
        """
        Prompt for a response and return the result.
        """

        # TEST
        return ''

    def get_input_with_choices(self, text: str, choices: typing.List[str],
            reprompt: bool = True,
            normalize_case: bool = True, check_command: bool = True) -> str:
        """
        Prompt for a response from a set of pre-defined choices and return the result.
        """

        # TEST
        return ''

    def check_and_run_command(self, line: str) -> bool:
        """
        Check if the line looks like a command, and run the associated command.
        Return true if the given line should be consumed (whether or not the command ran successfully).
        """

        line = line.strip()
        if (not line.startswith(self.command_prefix)):
            return False

        parts = re.split(r'\s+', line, maxsplit = 1)

        command_key = parts[0].removeprefix(self.command_prefix)
        if (len(command_key) == 0):
            self.write(f"ERROR: No command was provided after command prefix ('{self.command_prefix}').")
            return True

        argument = None
        if (len(parts) == 2):
            argument = parts[1]

        target_command = None
        for (keys, command) in self.commands.items():
            if (command_key in keys):
                target_command = command
                break

        if (target_command is None):
            self.write(f"ERROR: Command not found: '{command_key}'.")

            if (self.help_command_key is not None):
                self.write(f"{self.indent}Use `{self.command_prefix}{self.help_command_key}` to see the available commands.")

            return True

        target_command.run(self, argument)

        return True

    def read_line(self,
            display_prompt: bool = True,
            step_prompt: typing.Union[str, None] = None,
            ) -> typing.Union[str, None]:
        """
        Read the next line of input.
        Return None if there is no next line.
        """

        if (display_prompt and self.reader.isatty()):
            prompt = step_prompt
            if (prompt is None):
                prompt = self.prompt_text

            self.write(prompt, newline = False, flush = True)

        raw_line = self.reader.readline()

        # On an EOF/Ctrl-D the returned string will be empty.
        # On just an enter, it will be at least 1 (because of the newline).
        if (len(raw_line) == 0):
            raise EOFError('EOF on reading input line.')

        self.has_read_line = True
        return raw_line.strip()

    def _transition(self, current_step_index: typing.Union[int, None]) -> typing.Union[int, None]:
        """
        Transition to the next step in the wizard and return the new step's index.
        If there is no next step, return None.
        If the current step index is None, then start at the first step.
        """

        # Start at the first step.
        if (current_step_index is None):
            return 0

        # Transition out of the current step.
        self.steps[current_step_index].outro(self)

        current_step_index += 1

        if (current_step_index >= len(self.steps)):
            return None

        # Transition into the new step.
        self.steps[current_step_index].intro(self)

        return current_step_index

    def intro(self) -> None:
        """ Called before transitioning to the first step. """

    def help(self) -> None:
        """ Called when the user explicitly requests help. """

        lines = [
            'Available Commands:',
        ]

        for (keys, command) in sorted(self.commands.items()):
            keys_text = ', '.join([f"{self.command_prefix}{key}" for key in keys])
            lines.append(f"{self.indent}{keys_text} -- {command.help_line}")

        self.write(os.linesep.join(lines))

    def status(self) -> None:
        """ Called when the user explicitly requests the status of this wizard. """

        lines = [
            'Steps:',
        ]

        for (i, step) in enumerate(self.steps):
            status = step.status_line()
            if (status != ''):
                status = f" -- {status}"

            lines.append(f"{self.indent}{i + 1}: {step.name}{status}")

        self.write(os.linesep.join(lines))

    def clear(self) -> None:
        """ Called when the user explicitly requests to clear the wizard screen. """

        autograder.util.terminal.clear_screen(self.writer)

    def outro(self) -> None:
        """
        Called after transitioning out of the last step.
        Is NOT called on an early exit.
        """

    def early_exit(self) -> None:
        """
        Called when run() has exited early.
        Called instead of outro().
        """

        self.write("Wizard exited early.")
