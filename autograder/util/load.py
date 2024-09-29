# Read a TSV file and return a list of lists of the cleaned fields in the TSV file.
# Raise an error if a line has more fields than the maximum length.
def load_users(path, max_len):
    all_parts = []

    with open(path, 'r') as file:
        lineno = 0
        for line in file:
            lineno += 1

            line = line.strip()
            if (line == ""):
                continue

            parts = line.split("\t")
            parts = [part.strip() for part in parts]

            if (len(parts) > max_len):
                raise ValueError(
                    "File ('%s') line (%d) has too many values. Max is %d, found %d." % (
                        path, lineno, max_len, len(parts)))

            all_parts.append(parts)

    return all_parts
