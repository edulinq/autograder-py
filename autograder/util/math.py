import math
import typing

DEFAULT_FORMAT_PRECISION: int = 2

def number_to_str(
        number: typing.Union[int, float],
        precision: int = DEFAULT_FORMAT_PRECISION,
        exact_precision: bool = False,
        ) -> str:
    """
    Convert a number to a string.
    If the number is a float, use the given precision to round the number.

    When `exact_precision` is set, the input will be turned into an int and formatted with that exact precision.
    Otherwise, smallest precision possible will be used (while still keeping the value of the input).
    """

    precision = max(0, precision)

    if (not exact_precision):
        for effective_precision in range(precision):
            rounded_number: typing.Union[float, int] = round(number, effective_precision)
            if (math.isclose(number, rounded_number)):
                if (effective_precision == 0):
                    rounded_number = int(rounded_number)

                return str(rounded_number)

    return "{number:0.{precision}f}".format(number = round(float(number), precision), precision = precision)  # pylint: disable=consider-using-f-string
