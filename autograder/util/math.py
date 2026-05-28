import typing

def number_to_str(number: typing.Union[int, float], precision: int = 2) -> str:
    """
    Convert a number to a string.
    If the number is a float, use the given precision to round the number.
    """

    if (isinstance(number, int)):
        return str(number)

    return str(round(number, precision))
