import sys

# Control if exit_from_error() should actually exit.
# Testing infrastructure can set this to control exit behavior.
_exit_on_error_for_testing = True

def exit_from_error(exit_status = 1):
    """
    Exit because an error occurred.
    Tetsing infrastructure can set _exit_on_error_for_testing to false to avoid exiting.
    """

    if (not _exit_on_error_for_testing):
        return

    sys.exit(exit_status)

class AutograderError(Exception):
    pass

class APIError(AutograderError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code

class ConnectionError(AutograderError):
    pass
