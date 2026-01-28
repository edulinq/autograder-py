import contextlib
import logging
import os
import re
import sys
import typing

import edq.util.dirent
import flake8.api.legacy

import autograder.code
import autograder.question
import autograder.util.submission

DEFAULT_MAX_LINE_LENGTH: int = 150

# For codes, see:
# flake8: https://flake8.pycqa.org/en/latest/user/error-codes.html
# pycodestyle: https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes
BASE_STYLE_OPTIONS: typing.Dict[str, typing.Any] = {
    'max_line_length': DEFAULT_MAX_LINE_LENGTH,
    'max_doc_length': DEFAULT_MAX_LINE_LENGTH,
    'select': 'E,W,F',
    'show_source': True,
    'color': 'never',
    'ignore': [
        # Allow flexibility for function closing parens.
        'E123',
        'E124',

        # Don't force continuation line alignment.
        'E126',
        'E128',

        # Allow spaces around parameter/keyword equals.
        'E251',

        # Don't force two spaces between functions/class.
        # We only want one space.
        'E302',
        'E305',

        # Allow lambdas to be assigned into a local variable.
        'E731',

        # Ignore missing newlines at the end of the file.
        # This is a result of striping incoming code.
        'W292',

        # Do not enforce spaces in blank lines.
        # This should typically be enforced,
        # but because code from notebooks is hard to give a nice line number for
        # students have difficulty finding where the issue is.
        'W293',

        # PEP-8 recommends breaking a line before a binary operator.
        # This was a recent reversal of idiomatic Python.
        # W503 enforces the old style, while W504 enforces the new style.
        'W503',
    ]
}

class Style(autograder.question.Question):
    """
    A question that can be added to assignments that checks style.
    """

    def __init__(self,
            paths: typing.Union[str, typing.List[str], None] = None,
            ignore_paths: typing.Union[typing.List[str], None] = None,
            ignore_patterns: typing.Union[typing.Sequence[typing.Union[str, re.Pattern]], None] = None,
            max_points: float = 5,
            fake_path: typing.Union[str, None] = None,
            shorten_path: bool = True,
            style_overrides: typing.Union[typing.Dict[str, typing.Any], None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(max_points)

        if (paths is None):
            paths = []

        if (isinstance(paths, str)):
            paths = [paths]

        self._paths: typing.List[str] = paths
        """ The paths to check. """

        if (ignore_paths is None):
            ignore_paths = []

        self._ignore_paths = ignore_paths
        """
        Paths to ignore when checking style.
        These should be relative to where the style checker will be run or absolute.
        Use `ignore_patterns` for more flexiblity.
        """

        if (ignore_patterns is None):
            ignore_patterns = []

        clean_ignore_patterns = []
        for pattern in ignore_patterns:
            if (isinstance(pattern, re.Pattern)):
                clean_ignore_patterns.append(pattern)
            else:
                clean_ignore_patterns.append(re.compile(pattern))

        self._ignore_patterns = clean_ignore_patterns
        """ Patterns to check against every file path before making checks. """

        self._fake_path: typing.Union[str, None] = fake_path
        """
        A fake path to use when reporting style errors.
        This can help make output cleaner.
        """

        self._shorten_paths: bool = shorten_path
        """
        Shorten the reported path when reporting style errors.
        This can help make output cleaner.
        """

        if (style_overrides is None):
            style_overrides = {}

        self._style_overrides = style_overrides
        """ Overrides for options passed directly to flake8. """

    def score_question(self, submission: typing.Any, **kwargs: typing.Any) -> None:
        error_count, style_output = check_paths(
                self._paths,
                ignore_paths = self._ignore_paths,
                ignore_patterns = self._ignore_patterns,
                fake_path = self._fake_path,
                shorten_path = self._shorten_paths,
                style_overrides = self._style_overrides,
                include_clean_paths = False,
        )

        if (error_count == 0):
            self.full_credit(message = 'Style is clean!')
            return

        self.add_message(f"Code has {error_count} style issues (shown below). Note that line numbers may be offset in iPython notebooks.")
        self.set_score(max(0, self.max_points - error_count))

        self.add_message("--- Style Output BEGIN ---")
        for (path, lines) in style_output:
            self.add_message(f"\nStyle Issues for: '{path}':")
            self.add_message('---')
            self.add_message("\n".join(lines))
            self.add_message("---\n")
        self.add_message("--- Style Output END ---")

def check_path(
        path: str,
        **kwargs: typing.Any) -> typing.Tuple[int, typing.List[typing.Tuple[str, typing.List[str]]]]:
    """
    Check a single path for style.
    See check_paths() and check_file() for kwargs.
    See check_paths() for return value.
    """

    return check_paths([path], **kwargs)

def check_paths(
        paths: typing.List[str],
        ignore_paths: typing.Union[typing.List[str], None] = None,
        ignore_patterns: typing.Union[typing.Sequence[typing.Union[str, re.Pattern]], None] = None,
        include_clean_paths: bool = False,
        **kwargs: typing.Any) -> typing.Tuple[int, typing.List[typing.Tuple[str, typing.List[str]]]]:
    """
    Check the style of all the listed paths (recursively).

    If `include_clean_paths` is false, then no information is returned on empty files,
    otherwise, these files will be included in the results (with empty description lines).
    Ignored paths are never included in the results.

    Returns a two-item tuple of:
        - The total number of style violations.
        - A list of two-item tuples of:
            - The path to the context file.
            - A list of strings that describe the style issues in the context file.
    """

    if (ignore_paths is None):
        ignore_paths = []

    ignore_paths = [os.path.abspath(path) for path in ignore_paths]

    if (ignore_patterns is None):
        ignore_patterns = []

    clean_ignore_patterns = []
    for pattern in ignore_patterns:
        if (isinstance(pattern, re.Pattern)):
            clean_ignore_patterns.append(pattern)
        else:
            clean_ignore_patterns.append(re.compile(pattern))

    total_count = 0

    # [(path, lines), ...]
    total_lines = []

    for path in sorted(paths):
        path = os.path.abspath(path)

        skip = False

        for ignore_path in ignore_paths:
            if (path == ignore_path):
                skip = True
                break

        for ignore_pattern in clean_ignore_patterns:
            if (re.search(ignore_pattern, path) is not None):
                skip = True
                break

        if (skip):
            continue

        if (os.path.isfile(path)):
            if (os.path.splitext(path)[1] not in autograder.util.submission.ALLOWED_EXTENSIONS):
                continue

            count, raw_lines = check_file(path, **kwargs)
            lines = [(path, raw_lines)]
        else:
            dirents = [os.path.join(path, dirent) for dirent in os.listdir(path)]
            count, lines = check_paths(dirents,
                    ignore_paths = ignore_paths, ignore_patterns = ignore_patterns, include_clean_paths = include_clean_paths, **kwargs)

        if (include_clean_paths or (count > 0)):
            total_count += count
            total_lines += lines

    return total_count, total_lines

def check_file(
        path: str,
        fake_path: typing.Union[str, None] = None,
        shorten_path: bool = False,
        style_overrides: typing.Union[typing.Dict[str, typing.Any], None] = None,
        **kwargs: typing.Any) -> typing.Tuple[int, typing.List[str]]:
    """
    Check the style of a file.
    Return a two-item tuple of:
        - The number of style violations.
        - A list of strings that describe the style issues.
    """

    if (style_overrides is None):
        style_overrides = {}

    if (not os.path.isfile(path)):
        raise ValueError(f"Can only check style on a file, got a directory: '{path}'.")

    cleanup_paths = []

    if (path.endswith('.py')):
        pass
    elif (path.endswith('.ipynb')):
        contents = autograder.code.extract_notebook_code(path)

        temp_path = edq.util.dirent.get_temp_path(prefix = 'style_', suffix = '_notebook')
        cleanup_paths.append(temp_path)
        edq.util.dirent.write_file(temp_path, contents, strip = False, newline = False)

        path = temp_path
    else:
        raise ValueError(f"Can only check style on .py or .ipynb files, got '{path}'.")

    path = os.path.realpath(path)

    replacement_path = path

    if (fake_path is not None):
        replacement_path = fake_path

    if (shorten_path):
        replacement_path = os.path.basename(replacement_path)

    output_path = edq.util.dirent.get_temp_path(prefix = 'style_', suffix = '_output')
    cleanup_paths.append(output_path)

    # Ignore most flake8 logging.
    logging.getLogger("flake8").setLevel(logging.WARNING)

    # argparse (used by flake8) will look for a program name on sys.argv[0].
    if (len(sys.argv) == 0):
        sys.argv = ['']

    style_options = BASE_STYLE_OPTIONS.copy()
    style_options.update(style_overrides)

    style_guide = flake8.api.legacy.get_style_guide(**style_options)

    with open(output_path, 'w', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        with contextlib.redirect_stdout(file):
            report = style_guide.check_files([path])

    with open(output_path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lines = file.readlines()

    lines = [line.rstrip() for line in lines]

    if (path != replacement_path):
        lines = [line.replace(path, replacement_path) for line in lines]

    for cleanup_path in cleanup_paths:
        edq.util.dirent.remove(cleanup_path)

    return (report._application.result_count, lines)
