import io
import os
import subprocess
import sys
import typing

DEFAULT_TTY_CLEAR_NEWLINES: int = 200
DEFAULT_NONTTY_CLEAR_NEWLINES: int = 200

def clear_screen(
        writer: typing.Union[io.TextIOBase, None] = None,
        nontty_newline: int = DEFAULT_NONTTY_CLEAR_NEWLINES,
        tty_newline: int = DEFAULT_TTY_CLEAR_NEWLINES) -> None:
    """
    If the given writer is a terminal/tty (stdout by default),
    then attempt to clear it based on the current OS.
    If os-based clearing does not work, then fallback to printing the given number of newlines.
    """

    if (writer is None):
        writer = typing.cast(io.TextIOBase, sys.stdout)

    # If not pointing to a terminal, just print some newlines.
    if (not writer.isatty()):
        writer.write(os.linesep * nontty_newline)
        return

    # Try to use system commands to clear.
    success = False
    if (writer == sys.stdout):
        success = _clear_stdout()

    # Fallback to newlines.
    if (not success):
        writer.write(os.linesep * tty_newline)

def _clear_stdout() -> bool:
    """
    Try to clear stdout.
    Return if the attempt was successful (or at least didn't error).
    """

    command = None
    if (os.name == 'posix'):
        command = 'clear'
    elif (os.name == 'nt'):
        command = 'cls'
    else:
        return False

    result = subprocess.run(command, shell = True, check = False)
    return (result.returncode == 0)
