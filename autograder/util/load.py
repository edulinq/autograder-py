import typing

import edq.util.dirent

def load_tsv(path: str, max_len: int, min_len: int = 1) -> typing.List[typing.List[str]]:
    """
    Read a TSV file and return a list of lists of the stripped fields in the TSV file.
    Raise an error if a line has more fields than the maximum length
    or less fields than the minimum length.
    """

    rows = []

    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lineno = 0
        for line in file:
            lineno += 1

            line = line.strip()

            if (line == ""):
                continue

            row = line.split("\t")
            row = [field.strip() for field in row]

            if (len(row) < min_len):
                raise ValueError(f"File ('{path}') line ({lineno}) has too few values. Min is {min_len}, found {len(row)}.")

            if (len(row) > max_len):
                raise ValueError(f"File ('{path}') line ({lineno}) has too many values. Max is {max_len}, found {len(row)}.")

            rows.append(row)

    return rows
