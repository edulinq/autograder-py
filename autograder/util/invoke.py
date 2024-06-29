import multiprocessing
import sys
import time
import traceback

REAP_TIME_SEC = 5

# Return: (success, function return value)
# On timeout, success will be false and the value will be None.
# On error, success will be false and value will be the string stacktrace.
# On successful completion, success will be true and value may be None (if nothing was returned).
def with_timeout(timeout, function):
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

    result = multiprocessing.Queue(1)

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
        exception, stacktrace = error
        return (False, stacktrace)

    return (True, value)

def _invoke_helper(result, function):
    value = None
    error = None

    try:
        value = function()
    except Exception as ex:
        error = (ex, traceback.format_exc())

    sys.stdout.flush()

    result.put((value, error))
    result.close()
