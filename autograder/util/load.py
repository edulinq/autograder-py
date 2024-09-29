# Read a TSV file and return a list of lists of the stripped fields in the TSV file.
# Raise an error if a line has more fields than the maximum length
# or less fields than the minimum length.
def load_tsv(path, max_len, min_len = 1):
    rows = []

    with open(path, 'r') as file:
        lineno = 0
        for line in file:
            lineno += 1

            line = line.strip()

            if (line == ""):
                continue

            row = line.split("\t")
            row = [field.strip() for field in row]

            if (len(row) < min_len):
                raise ValueError(
                    "File ('%s') line (%d) has too few values. Min is %d, found %d." % (
                        path, lineno, min_len, len(row)))

            if (len(row) > max_len):
                raise ValueError(
                    "File ('%s') line (%d) has too many values. Max is %d, found %d." % (
                        path, lineno, max_len, len(row)))

            rows.append(row)

    return rows
