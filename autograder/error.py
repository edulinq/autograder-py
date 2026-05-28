import sys
import typing

_exit_on_error_for_testing: bool = True  # pylint: disable=invalid-name
"""
Control if exit_from_error() should actually exit.
Testing infrastructure can set this to control exit behavior.
"""

def exit_from_error(exit_status: int = 1) -> None:
    """
    Exit because an error occurred.
    Testing infrastructure can set _exit_on_error_for_testing to false to avoid exiting.
    """

    if (not _exit_on_error_for_testing):
        return

    sys.exit(exit_status)

class AutograderError(Exception):
    """ General errors from the autograder (including this interface). """

class APIError(AutograderError):
    """ Errors that specifically come from the autograder server. """

    def __init__(self, code: typing.Union[int, None], message: str) -> None:
        super().__init__(message)

        self.code: typing.Union[int, None] = code
        """ The HTTP status code. """

class ConnectionError(AutograderError):
    """ An error stemming from a bad network connection. """
