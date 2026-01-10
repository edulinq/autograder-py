import multiprocessing
import sys
import time
import traceback
import typing

REAP_TIME_SEC: float = 5

_multiprocessing_initialized: bool = False  # pylint: disable=invalid-name

def _init_multiprocessing() -> None:
    """
    Initialize Python multiprocessing.
    Note that this should only be called on Linux code paths.
    """

    global _multiprocessing_initialized  # pylint: disable=global-statement

    if (_multiprocessing_initialized):
        return

    multiprocessing.set_start_method('fork')
    _multiprocessing_initialized = True

def with_timeout(timeout: float, function: typing.Callable) -> typing.Tuple[bool, typing.Any]:
    """
    Run the given function in a differnet process with the given timeout.

    Return: (success, function return value)
    On timeout, success will be false and the value will be None.
    On error, success will be false and value will be the string stacktrace.
    On successful completion, success will be true and value may be None (if nothing was returned).
    """

    if (not sys.platform.startswith('linux')):
        # Mac and Windows have some pickling issues with multiprocessing.
        # Just run them without a timeout.
        # Any autograder will be run on a Linux machine and will be safe.
        start_time = time.time()
        value = function()
        runtime = time.time() - start_time

        if (runtime > timeout):
            return (False, None)

        return (True, value)

    _init_multiprocessing()

    result: multiprocessing.Queue = multiprocessing.Queue(1)

    # Note that we use processes instead of threads so they can be more completely killed.
    process = multiprocessing.Process(target = _invoke_helper, args = (result, function))
    process.start()

    # Wait for at most the timeout.
    process.join(timeout)

    # Check to see if the process is still running.
    if (process.is_alive()):
        # Kill the long-running process.
        process.terminate()

        # Try to reap the process once before just giving up on it.
        process.join(REAP_TIME_SEC)

        return (False, None)

    # Check to see if the process explicitly existed (like via sys.exit()).
    if (result.empty()):
        return (False, 'Code explicitly exited (like via sys.exit()).')

    value, error = result.get()

    if (error is not None):
        _, stacktrace = error
        return (False, stacktrace)

    return (True, value)

def _invoke_helper(result: multiprocessing.Queue, function: typing.Callable) -> None:
    """ A helper function for running the given function. """

    value = None
    error = None

    try:
        value = function()
    except Exception as ex:
        error = (ex, traceback.format_exc())

    sys.stdout.flush()

    result.put((value, error))
    result.close()
