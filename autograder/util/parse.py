import typing

def string_list(raw_value: typing.Any, delim: str = ', ') -> typing.List[str]:
    """ Parse a list of strings. """

    value = raw_value

    if (value is None):
        return []

    if (isinstance(value, (list, tuple))):
        return [str(item) for item in value]

    value = str(value).strip()

    if (len(value) == 0):
        return []

    if (len(value) == 1):
        raise ValueError(f"Cannot parse a list from this string, it is too short: '{raw_value}'.")

    # Strip opening and closing brackets.
    value = value[1:-1]

    if (len(value) == 0):
        return []

    items = []
    for item in value.split(delim):
        # Strip quotes.
        items.append(item[1:-1])

    return items
