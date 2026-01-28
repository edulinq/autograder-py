"""
Utilities for extracting and working with Python source code.
"""

import ast
import os
import sys
import types
import typing

import edq.util.dirent
import edq.util.json

DEFAULT_MODULE_AST_ALLOWED_NODES: typing.List[typing.Type] = [
    ast.Import,
    ast.ImportFrom,
    ast.FunctionDef,
    ast.ClassDef,
]

def extract_code(path: str) -> str:
    """
    Gets the source code out of a path (to either a notebook or vanilla python).
    All code will be cleaned in some way (for uncleaned code, just read the file normally).
    """

    code = None

    if (path.lower().endswith('.ipynb')):
        code = extract_notebook_code(path)
    elif (path.lower().endswith('.py')):
        code = extract_python_code(path)
    else:
        raise ValueError(f"Unknown extension for extracting code: '{path}'.")

    return code.strip()

def extract_python_code(path: str) -> str:
    """
    Gets the source code out of a Python code file.
    Each line will be stripped of trailing whitespace and joined with a single newline.
    This may change the contents of multiline strings.
    """

    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lines = file.readlines()

    lines = [line.rstrip() for line in lines]
    code = "\n".join(lines)

    return code.strip()

def extract_notebook_code(path: str) -> str:
    """
    Extract all the code cells from an iPython notebook.
    A concatenation of all the cells (with a newline between each cell) will be output.
    """

    notebook = edq.util.json.load_path(path, strict = True)

    contents = []
    for cell in notebook['cells']:
        if (cell['cell_type'] != 'code'):
            continue

        cell_code = ''.join(cell['source']).strip()

        # Ignore empty cells.
        if (cell_code == ''):
            continue

        contents.append(cell_code)

    return "\n".join(contents) + "\n"

def sanitize_and_import_path(path: str, **kwargs: typing.Any) -> typing.Any:
    """ Get the code from a source file and call sanitize_and_import_code() with it. """

    source_code = extract_code(path)
    return sanitize_and_import_code(source_code, code_path = path, **kwargs)

def sanitize_and_import_code(
        source_code: str,
        code_path: str = '<unspecified>',
        syspath: typing.Union[str, None] = None,
        **kwargs: typing.Any) -> typing.Any:
    """
    Sanitize the given code, exec it, and return it as a namespace or dict.
    The code is assumed to be a module.
    See parse_module_code() for sanitization details and kwargs.
    Prefer sanitize_and_import_path() over this function, because file and path information will be automatically set.
    """

    if (syspath is None):
        syspath = os.path.dirname(os.path.abspath(os.getcwd()))

    module_ast = parse_module_code(source_code, **kwargs)

    globals_defs: typing.Dict[str, typing.Any] = {}

    try:
        sys.path.append(syspath)
        exec(compile(module_ast, filename = code_path, mode = "exec"), globals_defs)  # pylint: disable=exec-used
    finally:
        sys.path.pop()

    return types.SimpleNamespace(**globals_defs)

def parse_module_code(
        source_code: str,
        sanitize: bool = True,
        allowed_module_nodes: typing.Union[typing.List[typing.Type], None] = None,
        **kwargs: typing.Any) -> ast.Module:
    """
    Parse a Python module's (file's) code, optionally sanitize it, and return an AST.
    Sanitization in this context means removing things that are not
    imports, functions, constants, and classes.
    A "constant" will be considered an assignment where the LHS is a single variable all in caps.
    """

    if (allowed_module_nodes is None):
        allowed_module_nodes = DEFAULT_MODULE_AST_ALLOWED_NODES

    module_ast = ast.parse(source_code)

    if (not isinstance(module_ast, ast.Module)):
        raise ValueError(f"Provided code for parsing is not a Python module, found: '{type(module_ast)}'.")

    if (not sanitize):
        return module_ast

    keep_nodes = []
    for node in module_ast.body:
        if (type(node) in DEFAULT_MODULE_AST_ALLOWED_NODES):
            keep_nodes.append(node)
            continue

        if (not isinstance(node, ast.Assign)):
            continue

        if ((len(node.targets) != 1) or (not isinstance(node.targets[0], ast.Name))):
            continue

        if (node.targets[0].id != node.targets[0].id.upper()):
            continue

        keep_nodes.append(node)

    module_ast.body = keep_nodes
    return module_ast

def ast_to_source(code_ast: ast.AST) -> str:
    """ Get code from a Python AST. """

    return ast.unparse(code_ast)
