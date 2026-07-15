import sys
import typing

def print_no_match(label: str, query: typing.Union[typing.Any, None] = None) -> None:
    """ Print a "no matching X found" error message to stdout. """

    if (query is not None):
        query = str(query)

        if (len(query) == 0):
            query = None

    message = f"No matching {label} found."
    if (query is not None):
        message = f"No matching {label} found: '{query}'."

    print(message, file = sys.stderr)
